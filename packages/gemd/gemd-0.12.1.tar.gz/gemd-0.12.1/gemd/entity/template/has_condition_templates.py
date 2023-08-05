"""For entities that have a condition template."""
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.setters import validate_list
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.template.condition_template import ConditionTemplate


class HasConditionTemplates(object):
    """
    Mixin-trait for entities that include condition templates.

    Parameters
    ----------
    conditions: List[ConditionTemplate]
        A list of this entity's condition templates.

    """

    def __init__(self, conditions):
        self._conditions = None
        self.conditions = conditions

    @property
    def conditions(self):
        """
        Get the list of condition templates.

        Returns
        -------
        List[ConditionTemplate]
            List of this entity's condition templates

        """
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        lst = validate_list(conditions, (ConditionTemplate, LinkByUID, list, tuple))

        # make sure attribute can be a Condition
        # TODO: list.map(_.validate_scope(AttributeType.CONDITION)) all true

        self._conditions = list(map(BaseTemplate._homogenize_ranges, lst))
