import lxml.html
import swapper
from django.http import Http404, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, View
from lxml import etree
from lxml.builder import E

ReportTemplate = swapper.load_model("mrrt", "ReportTemplate")


@method_decorator(csrf_exempt, name="dispatch")
class ReportTemplateView(View):
    """
    Implements:
    - RAD-103 "Retrieve Imaging Report Template" transaction.
    - RAD-104 "Store Imaging Report Template" transaction.
    """

    model = ReportTemplate
    # queryset = None
    template_uid_url_kwarg = "templateUID"  # Match the case of the spec
    template_uid_field = "template_uid"

    def get(self, request, *args, **kwargs):
        """
        RAD-103 "Retrieve Imaging Report Template" transaction.

        Returns the template via a GET for a specific templateUID.
        """

        self.object = self.get_object()
        return self.render_to_response({"object": self.object})

    def put(self, request, *args, **kwargs):
        """
        RAD-104 "Store Imaging Report Template" transaction.

        Saves or Updates the template via a PUT for a specific templateUID.
        """

        # TODO check template_uid == dcterms.identifier -> 400
        # TODO 422 – Unprocessable Entity. This indicates that the Responder was unable
        #      to store the template because the template does not conform to RAD
        #      TF-3: 8.1
        # TODO 401 - Unauthorized

        lookup_kwargs = self.get_object_lookup_kwargs()
        # template_uid =

        content = self.request.body
        # root = etree.fromstring(content)#, etree.HTMLParser())
        doc = etree.XML(self.request.body)

        print(doc)
        # print(dir(doc))
        # print(doc.docinfo.encoding)
        # print(etree.tostring(doc))

        encoding = doc.xpath("/html/head/meta/@charset")[0]
        identifier = doc.xpath('/html/head/meta[@name="dcterms.identifier"]/@content')[
            0
        ]
        # FIXME compar to <title>
        title = doc.xpath('/html/head/meta[@name="dcterms.title"]/@content')[0]
        description = doc.xpath(
            '/html/head/meta[@name="dcterms.description"]/@content'
        )[0]

        assert identifier == lookup_kwargs[self.template_uid_field]

        obj, created = self.model.objects.update_or_create(
            # FIXME use cleaned document?
            defaults={
                "content": content.decode(encoding),
                "description": description,
                "title": title,
            },
            **lookup_kwargs,
        )
        return HttpResponse("ok")

    def get_queryset(self):
        if self.queryset is None:
            return self.model._default_manager.all()
        return self.queryset.all()

    def get_object_lookup_kwargs(self):
        template_uid = self.kwargs.get(self.template_uid_url_kwarg)

        if template_uid is None:
            raise AttributeError(
                f"View {self.__class__.__name} must be called"
                f" with {self.template_uid_url_kwarg}."
            )

        return {self.template_uid_field: template_uid}

    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.
        Require `self.queryset` and a `template_uid` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        queryset = queryset.filter(**self.get_object_lookup_kwargs())

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                f"No {queryset.model._meta.verbose_name} found matching the query"
            )

        return obj

    def render_to_response(self, context):
        return HttpResponse(self.object.content, content_type="text/html")

    # TODO
    # def template_valid():
    #     Per spec, the sender may perform <header> updates using the same templateUID,
    #     but <body> updates should receive a new templateUID.  This view does **not**
    #     currently enforce that behaviour and expects the sender to per the spec.


class ReportTemplatesListView(ListView):
    model = ReportTemplate

    def to_template(self, obj):
        # WARN: we "cheat" and pick out the <head>, while the spec technically indicates
        #  that specific fields are copied here
        # PERF: storing raw elements may be faster than parsing out the head
        doc = etree.XML(obj.content)
        head = doc.xpath("/html/head")

        return E.template(
            *head[0].getchildren(),
            href=self.request.build_absolute_uri(obj.get_absolute_url()),
        )

    def render_to_response(self, context):
        doc = E.templates(*[self.to_template(obj) for obj in self.object_list])
        xml = etree.tostring(doc, xml_declaration=True, encoding="UTF-8")
        return HttpResponse(xml, content_type="text/xml")
