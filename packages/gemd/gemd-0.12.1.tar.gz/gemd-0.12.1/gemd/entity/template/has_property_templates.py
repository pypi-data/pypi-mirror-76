"""For entities that have a property template."""
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.setters import validate_list
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.template.property_template import PropertyTemplate


class HasPropertyTemplates(object):
    """
    Mixin-trait for entities that include property templates.

    Parameters
    ----------
    properties: List[PropertyTemplate]
        A list of this entity's property templates.

    """

    def __init__(self, properties):
        self._properties = None
        self.properties = properties

    @property
    def properties(self):
        """
        Get the list of property templates.

        Returns
        -------
        List[PropertyTemplate]
            List of this entity's property templates

        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        # make sure the properties are a list
        lst = validate_list(properties, (PropertyTemplate, LinkByUID, list, tuple))

        # make sure attribute can be a Property
        # TODO: list.map(_.validate_scope(AttributeType.PROPERTY)) all true

        # convert any templates into (template, bounds) pairs and
        # validate that any (template, bounds) pairs are consistent
        self._properties = list(map(BaseTemplate._homogenize_ranges, lst))
