import logging
import os
import shutil

from aqt import gui_hooks
from aqt import mw

import markdown

from KBjoint.kb import KB
from .lib.pymdownx.arithmatex import ArithmatexExtension


kb_dir = r'D:\Projects\.test\KB-test'


def reset_test_kb():
    for root, dirs, files in os.walk(kb_dir):
        if root.endswith('.backup'):
            for file in files:
                # Copy a file, replace if destination file already exist
                shutil.copy(
                    os.path.join(root, file),
                    os.path.join(os.path.dirname(root), file)
                )
    # Delete a file
    # os.remove(file_to_delete)


def remove_test_model():
    mm = mw.col.models
    mm.remove(mm.id_for_name('Cloze traceable (test)'))


def output_model():
    # todo write to file rather than logging, do not use logging in test modules
    logging.info('\n' +
                 str(mw.col.models.by_name('Cloze traceable (test)'))
                 )


def kb_join_test():
    """
    Join your knowledge base to Anki
    """
    reset_test_kb()
    remove_test_model()
    KB(top_dir=kb_dir, test_mode=True).join()
    # KB(top_dir=os.path.join(kb_dir, 'BlahBlah')).join()


text = r"""
This is inline $\left\{\frac{1}{n^2}\right\}$
but this is displayed 

$$
\int_0^1\frac{x^4(1-x)^4}{1+x^2}\,dx =\frac{22}{7}-\pi
$$

centred on its own line.
"""


def test_pymd_extension():
    math_extension = ArithmatexExtension()
    math_extension.config['preview'] = [False, ""]
    math_extension.config['generic'] = [True, ""]
    html = markdown.markdown(text, extensions=[math_extension])
    logging.info(html)


# gui_hooks.profile_did_open.append(output_model)
gui_hooks.profile_did_open.append(kb_join_test)
# gui_hooks.profile_did_open.append(test_pymd_extension)

