import json
import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
import subprocess

logger = logging.getLogger(__name__)


class DemoExtension(Extension):
    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument()
        logger.info("preferences %s" % json.dumps(extension.preferences))
        result = subprocess.run(
            ["qalc", query], stdout=subprocess.PIPE, text=True
        ).stdout
        items = [
            ExtensionResultItem(
                icon="images/icon.svg",
                name=result,
                description="Enter to copy the result\nAlt-enter to copy the expression",
                on_enter=CopyToClipboardAction(RunScriptAction("qalc -t %s" % query)),
                on_alt_enter=CopyToClipboardAction(result),
            )
        ]

        return RenderResultListAction(items)


if __name__ == "__main__":
    DemoExtension().run()
