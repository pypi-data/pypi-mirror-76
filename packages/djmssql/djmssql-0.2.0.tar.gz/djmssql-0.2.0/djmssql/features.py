from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.utils import InterfaceError
from django.utils.functional import cached_property


class DatabaseFeatures(BaseDatabaseFeatures):
    allow_sliced_subqueries_with_in = False
    can_introspect_autofield = True
    can_introspect_small_integer_field = True
    can_return_id_from_insert = True
    for_update_after_from = True
    has_real_datatype = True
    has_zoneinfo_database = False
    can_introspect_binary_field = True
    introspected_boolean_field_type = 'IntegerField'
    can_introspect_duration_field = False
    ignores_table_name_case = True
    ignores_quoted_identifier_case = True
    requires_literal_defaults = True
    requires_sqlparse_for_splitting = False
    supports_partially_nullable_unique_constraints = False
    supports_nullable_unique_constraints = False
    supports_paramstyle_pyformat = False
    supports_regex_backreferencing = False
    supports_sequence_reset = False
    supports_subqueries_in_group_by = False
    supports_temporal_subtraction = True
    supports_timezones = False
    supports_transactions = True
    uses_savepoints = True
    has_native_uuid_field = True
    has_select_for_update = False
    supports_table_check_constraints = False
    supports_tablespaces = False
    supports_index_on_text_field = False
    nulls_order_largest = False
    supports_json_field = False
    has_bulk_insert = False
    can_create_inline_fk = False
    allows_auto_pk_0 = False
    supports_unspecified_pk = True
    supports_select_union = False
    closed_cursor_error_class = InterfaceError
    supports_boolean_expr_in_select_clause = False

    @cached_property
    def introspected_field_types(self):
        return {
            **super().introspected_field_types,
            'BinaryField': 'TextField',
            'BooleanField': 'IntegerField',
            'DurationField': 'BigIntegerField',
            'GenericIPAddressField': 'CharField',
            'PositiveBigIntegerField': 'BigIntegerField',
            'PositiveIntegerField': 'IntegerField',
            'PositiveSmallIntegerField': 'SmallIntegerField',
        }
