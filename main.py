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
        expression = subprocess.run(
            ["qalc", query], stdout=subprocess.PIPE, text=True
        ).stdout
        result = subprocess.run(
            ["qalc", '-t', query], stdout=subprocess.PIPE, text=True
        ).stdout
        items = [
            ExtensionResultItem(
                icon="images/icon.svg",
                name=result.strip(),
                description=expression.strip(),
                on_enter=CopyToClipboardAction(result),
                on_alt_enter=CopyToClipboardAction(expression),
            )
        ]

        return RenderResultListAction(items)


if __name__ == "__main__":
    DemoExtension().run()
