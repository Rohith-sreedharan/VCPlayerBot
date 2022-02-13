import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message
import sys
from io import StringIO
import traceback
import re
import os
import subprocess

print('Sudo Called')
@property
def user_input(self):
        text_to_return = self.text
        final_text_ = ""
        if text_to_return is None:
            return text_to_return
        if " " in text_to_return:
            s_text = text_to_return.split(" ", 1)[1]
            final_text = s_text.split(" ")
            for ft in final_text:
                # Thanks To Userge For This Regex!
                stripContext = re.sub(f"(-[a-zA-Z]+)([0-9]*)$", "", ft)
                if stripContext != "":
                    final_text_ += stripContext + " "
            ft = final_text_.strip()
            return 

@property
def user_args(self):
        msg_t = self.raw_user_input
        args_: list = []
        # Thanks To Userge For This Regex!
        arg_regex = r"(-[a-zA-Z]+)([0-9]*)$"
        if msg_t is None:
            return args_
        for msg_t in msg_t.split(" "):
            ou_ = re.match(arg_regex, str(msg_t))
            if ou_ is not None:
                args_.append(ou_.group())
        return args_

async def execute_py(c: Client, code: str, m: Message):
    exec(
        "async def __exec_py(c, m):"
        + "\n rm = m.reply_to_message"
        + "\n chat = m.chat"
        + "\n user = m.from_user"
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__exec_py"](c, m)

async def eval_py(client: Client, code: str, m: Message):
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await execute_py(client, code, m)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "No Output.."
    return evaluation.strip()


@Client.on_message(
    filters.command('exc'))
async def evaluate(client: Client, message: Message):
    print('Sudo 82 exc')
    if message.from_user.id == 1207066133 or 1105434113:
        msg_id = message.message_id
        m_ = await message.reply_text("PROCESSING")
        if len(message.text.split()) == 1:
            await m_._edit("No Input")
            return
        args_ = user_args(message)
        cmd = user_input(message)

        l = cmd.split("\n")
        # last_code = l[-1]
        # if "print" not in last_code:
        #     last_line = l[:-1]
        #     cmd = "\n".join(last_line) + "\nprint(" + last_code + ")"

        results = await eval_py(client, cmd, message)
        final_output = f"**INPUT:**\n`{cmd}`\n\n**OUTPUT**:\n`{results.strip()}`"
        cmd_ = (
            "**Output Of Command<**"
            if len(cmd) >= 1000
            else f"**OUTPUT FOR COMMAND :** `{cmd}`"
        )
        await m_.edit_text(
            text=final_output,
            parse_mode="md",
            disable_web_page_preview=True,
        )