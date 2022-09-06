import swapper
from django.db import models
from django.urls import reverse


# Provide an abstract version of the model so that other projects could provide
# alternative concrete implementations (e.g. with versioning, multitenancy, etc)
class AbstractReportTemplate(models.Model):
    # Partial set of fields defined by "8.1 Report Template Structure"

    # template_uid is functionally unique, but defer to concrete implementations'
    #   meta.constraints to allow more complex relationships (e.g.
    #   customer + template_uid)
    template_uid = models.TextField(
        help_text=(
            "A unique alphanumeric identifier (OID) included in adny report instance "
            "generated using the template"
        )
    )

    title = models.TextField(
        help_text=(
            "A human readable name for the template. There is enforced "
            "correspondence with the title element in the head."
        )
    )

    # FIXME status

    content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.template_uid

    class Meta:
        abstract = True

    def get_absolute_url(self):
        """
        Subclasses should override if the reverse URL depends upon more than just
        the template_uid
        """
        return reverse("mrrt-template", kwargs={"templateUID": self.template_uid})


class ReportTemplate(AbstractReportTemplate):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["template_uid"], name="unique_template_uid")
        ]
        swappable = swapper.swappable_setting("mrrt", "ReportTemplate")
