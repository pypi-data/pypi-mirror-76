import datetime
import importlib
import keyword
import logging
import os
import re
from collections import OrderedDict

from django.db import DEFAULT_DB_ALIAS, connections, models
from django.db.models.constants import LOOKUP_SEP


logger = logging.getLogger('mountainred')
MIXIN = None


def get_mixin():
    settings = importlib.import_module(
        dict(os.environ)['DJANGO_SETTINGS_MODULE'])

    if hasattr(settings, "MIXIN_MODEL"):
        try:
            mixin = importlib.import_module(settings.MIXIN_MODEL)
            return mixin
        except:
            logger.error('mixin 路径错误，无法动态导入')
            return None
    else:
        return None


class MetaReflexError(BaseException):
    pass


class MetaReflex:
    """
    利用元编程将任意指定库表，
    反向动态生成Django.db.models类
    """

    # db_module = 'django.db'
    def __init__(self, BaseModel: object):

        MetaReflex.BASE_MODEL = BaseModel

    def handle_inspection(self, options):
        connection = connections[options['database']]
        # 'table_name_filter' is a stealth option
        table_name_filter = options.get('table_name_filter')

        def table2model(table_name):
            name = re.sub(r'[^a-zA-Z0-9]', '', table_name.title())
            if name:
                return name
            return table_name

        with connection.cursor() as cursor:
            # yield 'from %s import models' % self.db_module
            known_models = []
            table_info = connection.introspection.get_table_list(cursor)

            # Determine types of tables and/or views to be introspected.
            types = {'t'}
            if options['include_partitions']:
                types.add('p')
            if options['include_views']:
                types.add('v')

            for table_name in (options['table'] or sorted(info.name for info in table_info if info.type in types)):
                if table_name_filter is not None and callable(table_name_filter):
                    if not table_name_filter(table_name):
                        continue
                try:
                    try:
                        relations = connection.introspection.get_relations(
                            cursor, table_name)
                    except NotImplementedError:
                        relations = {}
                    try:
                        constraints = connection.introspection.get_constraints(
                            cursor, table_name)
                    except NotImplementedError:
                        constraints = {}
                    primary_key_column = connection.introspection.get_primary_key_column(
                        cursor, table_name)
                    unique_columns = [
                        c['columns'][0] for c in constraints.values()
                        if c['unique'] and len(c['columns']) == 1
                    ]
                    table_description = connection.introspection.get_table_description(
                        cursor, table_name)
                except Exception as e:
                    yield "# Unable to inspect table '%s'" % table_name
                    yield "# The error was: %s" % e
                    continue

                yield ''
                yield ''
                # 此处混入类的继承
                yield f'class {table2model(table_name)}(MetaReflex.BASE_MODEL):'

                known_models.append(table2model(table_name))
                used_column_names = []  # Holds column names used in the table so far
                column_to_field_name = {}  # Maps column names to names of model fields
                for row in table_description:
                    # Holds Field notes, to be displayed in a Python comment.
                    comment_notes = []
                    # Holds Field parameters such as 'db_column'.
                    extra_params = OrderedDict()
                    column_name = row.name
                    is_relation = column_name in relations

                    att_name, params, notes = self.normalize_col_name(
                        column_name, used_column_names, is_relation)
                    extra_params.update(params)
                    comment_notes.extend(notes)

                    used_column_names.append(att_name)
                    column_to_field_name[column_name] = att_name

                    # Add primary_key and unique, if necessary.
                    if column_name == primary_key_column:
                        extra_params['primary_key'] = True
                    elif column_name in unique_columns:
                        extra_params['unique'] = True

                    #  去除外键关联关系
                    # if is_relation:
                    #     rel_to = (
                    #         "self" if relations[column_name][1] == table_name
                    #         else table2model(relations[column_name][1])
                    #     )
                    #     if rel_to in known_models:
                    #         field_type = 'ForeignKey(%s' % rel_to
                    #     else:
                    #         field_type = "ForeignKey('%s'" % rel_to
                    # else:
                        # Calling `get_field_type` to get the field type string and any
                        # additional parameters and notes.
                    field_type, field_params, field_notes = self.get_field_type(
                        connection, table_name, row)
                    extra_params.update(field_params)
                    comment_notes.extend(field_notes)

                    field_type += '('

                    # Don't output 'id = meta.AutoField(primary_key=True)', because
                    # that's assumed if it doesn't exist.
                    if att_name == 'id' and extra_params == {'primary_key': True}:
                        if field_type == 'AutoField(':
                            continue
                        elif field_type == 'IntegerField(' and not connection.features.can_introspect_autofield:
                            comment_notes.append('AutoField?')

                    # Add 'null' and 'blank', if the 'null_ok' flag was present in the
                    # table description.
                    if row.null_ok:  # If it's NULL...
                        extra_params['blank'] = True
                        extra_params['null'] = True

                    field_desc = '%s = %s%s' % (
                        att_name,
                        # Custom fields will have a dotted path
                        '' if '.' in field_type else 'models.',
                        field_type,
                    )
                    if field_type.startswith('ForeignKey('):
                        field_desc += ', models.DO_NOTHING'

                    if extra_params:
                        if not field_desc.endswith('('):
                            field_desc += ', '
                        field_desc += ', '.join('%s=%r' % (k, v)
                                                for k, v in extra_params.items())
                    field_desc += ')'
                    if comment_notes:
                        field_desc += '  # ' + ' '.join(comment_notes)
                    yield '    %s' % field_desc
                is_view = any(info.name == table_name and info.type ==
                              'v' for info in table_info)
                is_partition = any(
                    info.name == table_name and info.type == 'p' for info in table_info)
                for meta_line in self.get_meta(options['database'], table_name, constraints, column_to_field_name, is_view, is_partition):
                    yield meta_line

                for method_line in self.mixin_method():
                    yield method_line

    def normalize_col_name(self, col_name, used_column_names, is_relation):
        """
        Modify the column name to make it Python-compatible as a field name
        """
        field_params = {}
        field_notes = []

        new_name = col_name.lower()
        if new_name != col_name:
            field_notes.append('Field name made lowercase.')

        if is_relation:
            if new_name.endswith('_id'):
                new_name = new_name[:-3]
            else:
                field_params['db_column'] = col_name

        new_name, num_repl = re.subn(r'\W', '_', new_name)
        if num_repl > 0:
            field_notes.append(
                'Field renamed to remove unsuitable characters.')

        if new_name.find(LOOKUP_SEP) >= 0:
            while new_name.find(LOOKUP_SEP) >= 0:
                new_name = new_name.replace(LOOKUP_SEP, '_')
            if col_name.lower().find(LOOKUP_SEP) >= 0:
                # Only add the comment if the double underscore was in the original name
                field_notes.append(
                    "Field renamed because it contained more than one '_' in a row.")

        if new_name.startswith('_'):
            new_name = 'field%s' % new_name
            field_notes.append("Field renamed because it started with '_'.")

        if new_name.endswith('_'):
            new_name = '%sfield' % new_name
            field_notes.append("Field renamed because it ended with '_'.")

        if keyword.iskeyword(new_name):
            new_name += '_field'
            field_notes.append(
                'Field renamed because it was a Python reserved word.')

        if new_name[0].isdigit():
            new_name = 'number_%s' % new_name
            field_notes.append(
                "Field renamed because it wasn't a valid Python identifier.")

        if new_name in used_column_names:
            num = 0
            while '%s_%d' % (new_name, num) in used_column_names:
                num += 1
            new_name = '%s_%d' % (new_name, num)
            field_notes.append('Field renamed because of name conflict.')

        if col_name != new_name and field_notes:
            field_params['db_column'] = col_name

        return new_name, field_params, field_notes

    def get_field_type(self, connection, table_name, row):
        """
        Given the database connection, the table name, and the cursor row
        description, this routine will return the given field type name, as
        well as any additional keyword parameters and notes for the field.
        """
        field_params = OrderedDict()
        field_notes = []

        try:
            field_type = connection.introspection.get_field_type(
                row.type_code, row)
        except KeyError:
            field_type = 'TextField'
            field_notes.append('This field type is a guess.')

        # Add max_length for all CharFields.
        if field_type == 'CharField' and row.internal_size:
            field_params['max_length'] = int(row.internal_size)

        if field_type == 'DecimalField':
            if row.precision is None or row.scale is None:
                field_notes.append(
                    'max_digits and decimal_places have been guessed, as this '
                    'database handles decimal fields as float')
                field_params['max_digits'] = row.precision if row.precision is not None else 10
                field_params['decimal_places'] = row.scale if row.scale is not None else 5
            else:
                field_params['max_digits'] = row.precision
                field_params['decimal_places'] = row.scale

        if field_type == 'GeometryField':
            # Getting a more specific field type and any additional parameters
            # from the `get_geometry_type` routine for the spatial backend.
            field_type, geo_params = connection.introspection.get_geometry_type(
                table_name, row)
            field_params.update(geo_params)

        return field_type, field_params, field_notes

    def get_meta(self, db_alias, table_name, constraints, column_to_field_name, is_view, is_partition):
        """
        Return a sequence comprising the lines of code necessary
        to construct the inner Meta class for the model corresponding
        to the given database table name.
        """
        unique_together = []
        has_unsupported_constraint = False
        for params in constraints.values():
            if params['unique']:
                columns = params['columns']
                if None in columns:
                    has_unsupported_constraint = True
                columns = [x for x in columns if x is not None]
                if len(columns) > 1:
                    unique_together.append(
                        str(tuple(column_to_field_name[c] for c in columns)))
        if is_view:
            managed_comment = "  # Created from a view. Don't remove."
        elif is_partition:
            managed_comment = "  # Created from a partition. Don't remove."
        else:
            managed_comment = ''
        meta = ['']
        if has_unsupported_constraint:
            meta.append('    # A unique constraint could not be introspected.')
        meta += [
            '    class Meta:',
            '        managed = False%s' % managed_comment,
            '        db_table = %r' % table_name,
        ]
        if unique_together:
            tup = '(' + ', '.join(unique_together) + ',)'
            meta += ["        unique_together = %s" % tup]

        # 添加 app_label
        meta += ["        app_label = '%s'" % db_alias]
        return meta

    def mixin_method(self) -> list:
        global MIXIN
        MIXIN = get_mixin()
        method = ['']
        if MIXIN:
            method += [
                "    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):"]
            method += ["        MIXIN.before_save(self)"]
            method += ["        super().save(force_insert=False, force_update=False, using=None, update_fields=None)"]
            method += ["        MIXIN.after_save(self)\n"]
            method += ["    def delete(self, using=None, keep_parents=False):"]
            method += ["        MIXIN.before_delete(self)"]
            method += ["        super().delete(using=None, keep_parents=False)"]
            method += ["        MIXIN.after_delete(self)"]

        return method


def gen_model_meta_code(table_name: str, db_alias: str, model_name: str) -> str:
    """根据指定表名称，库名称，利用元编程将生成的模型名称以model_name注入到全局变量.

    Arguments:
        table_name {str} -- 表名称
        db_alias {str} -- 数据库连接别名
        model_name {str} -- 模型局部或全局变量名

    Returns:
        str -- [description]
    """

    mr = MetaReflex()

    options = {
        'include_partitions': True,
        "include_views": True,
        "table": [table_name],
        "database":  db_alias
    }
    meta_code = ''
    # 迭代生成模型描述代码
    for i in mr.handle_inspection(options):
        meta_code += f'{i}\n'

    # meta_code += "%s = %s\n" % (model_name, meta_code.split(
    #     '(', 1)[0].replace('class ', '').replace('\n', ''))

    _model = None
    meta_code += "_model = %s\n" % meta_code.split(
        '(', 1)[0].replace('class ', '').replace('\n', '')
    logger.debug(meta_code)
    from django.db import models
    exec(meta_code, dict(models=models, _model=_model))
    # 返回最终的模型描述代码
    return _model


def table2model(table_name: str, db_alias: str, super_class: object = models.Model) -> models.Model:
    """根据指定表名称，库名称，利用元编程将生成的模型名称以model_name注入到全局变量.

    Arguments:
        table_name {str} -- 表名称
        db_alias {str} -- 数据库连接别名
        model_name {str} -- 模型局部或全局变量名
        super_class: {str} -- 继承自的父类的类名

    Returns:
        str -- [description]
    """

    mr = MetaReflex(super_class)

    options = {
        'include_partitions': True,
        "include_views": True,
        "table": [table_name],
        "database":  db_alias
    }
    meta_code = ''
    # 迭代生成模型描述代码
    for i in mr.handle_inspection(options):
        meta_code += f'{i}\n'

    logger.debug(meta_code)
    exec(meta_code)
    _model = eval("%s\n" % meta_code.split(
        '(', 1)[0].replace('class ', '').replace('\n', ''))

    return _model
