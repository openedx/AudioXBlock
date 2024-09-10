"""TO-DO: This XBlock will play an MP3 file as an HTML5 audio element. """


from xblock.core import XBlock
from xblock.fields import Integer, Scope, String
from xblock.fragment import Fragment
try:
    from xblock.utils.resources import ResourceLoader
except ModuleNotFoundError:  # For backward compatibility with releases older than Quince.
    from xblockutils.resources import ResourceLoader

resource_loader = ResourceLoader(__name__)


def _(text):
    """
    Make `_` a no-op, so we can scrape strings
    """
    return text


class AudioXBlock(XBlock):
    """
    This XBlock will play an MP3 file as an HTML5 audio element. 
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    src = String(
           scope=Scope.settings,
           help=_("URL for MP3 file to play"),
        )

    @staticmethod
    def resource_string(path):
        """Handy helper for getting resources from our kit."""
        return resource_loader.load_unicode(path)

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the AudioXBlock, shown to students
        when viewing courses.
        """
        frag = Fragment()
        frag.add_content(resource_loader.render_django_template(
            'templates/html/audio.html',
            context={
                'src': self.src,
            },
            i18n_service=self.runtime.service(self, 'i18n'),
        ))
        frag.add_css(self.resource_string("static/css/audio.css"))
        return frag

    def studio_view(self, context):
        """
        The view for editing the AudioXBlock parameters inside Studio.
        """
        frag = Fragment()
        frag.add_content(resource_loader.render_django_template(
            'templates/html/audio_edit.html',
            context={
                'src': self.src,
            },
            i18n_service=self.runtime.service(self, 'i18n'),
        ))
        js = self.resource_string("static/js/src/audio_edit.js")
        frag.add_javascript(js)
        frag.initialize_js('AudioEditBlock')

        return frag

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.src = data.get('src')

        return {'result': 'success'}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("AudioXBlock",
             """<vertical_demo>
                  <audio src="http://localhost/Ikea.mp3"> </audio>
                  <audio src="http://localhost/skull.mp3"> </audio>
                  <audio src="http://localhost/monkey.mp3"> </audio>
                </vertical_demo>
             """),
        ]
