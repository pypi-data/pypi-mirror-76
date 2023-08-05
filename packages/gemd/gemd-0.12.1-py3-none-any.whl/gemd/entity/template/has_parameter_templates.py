"""For entities that have a parameter template."""
from gemd.entity.link_by_uid import LinkByUID
from gemd.entity.setters import validate_list
from gemd.entity.template.base_template import BaseTemplate
from gemd.entity.template.parameter_template import ParameterTemplate


class HasParameterTemplates(object):
    """
    Mixin-trait for entities that include parameter templates.

    Parameters
    ----------
    parameters: List[ParameterTemplate]
        A list of this entity's parameter templates.

    """

    def __init__(self, parameters):
        self._parameters = None
        self.parameters = parameters

    @property
    def parameters(self):
        """
        Get the list of parameter templates.

        Returns
        -------
        List[ParameterTemplate]
            List of this entity's parameter templates

        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        lst = validate_list(parameters, (ParameterTemplate, LinkByUID, list, tuple))

        # make sure attribute can be a Parameter
        # TODO: list.map(_.validate_scope(AttributeType.PARAMETER)) all true

        self._parameters = list(map(BaseTemplate._homogenize_ranges, lst))
