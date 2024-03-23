import logging
import os.path

from aqt import gui_hooks
from aqt import mw

from ..kb import KB

kb_dir = r'D:\Projects\.test\KB-test'


def output_model():
    logging.info('\n' +
                 str(mw.col.models.by_name('Cloze (traceable)'))
                 )


# gui_hooks.profile_did_open.append(output_model)


def kb_join_test():
    """
    Join your knowledge base to Anki
    """
    KB(top_dir=kb_dir).join()
    # KB(top_dir=os.path.join(kb_dir, 'BlahBlah')).join()


gui_hooks.profile_did_open.append(kb_join_test)

