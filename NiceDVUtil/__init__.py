import os
from nicegui import ui, events
from local_file_picker import local_file_picker
from encoding import EncodeFile

__basedir__ = os.path.dirname(os.path.abspath(__file__))
_filename = {'filename': ''}

delete = ui.button()


ui.label("Super NiceDVUtil Application!")


with ui.dialog().props('full-width') as dialog:
    with ui.card():
        content = ui.markdown()


async def pick_file() -> None:
    global delete
    result = await local_file_picker(__basedir__, _filter="*.fhx")
    ui.notify(f'You chose {result}')
    _filename.update(filename=result)
    if result is not None:
        delete.enable()


def write_to_file(data, outfile):
    """
    https://github.com/zauberzeug/nicegui/issues/585#issuecomment-1490738443
    File created from input data.  Binary data from .fhx upload.
    :param. data,  uploaded byte data
    :return None"""

    if outfile != '':
        filecount = 0
        filenm = outfile[:(outfile.rfind("."))]
        fileext = outfile[(outfile.rfind(".")):]

        try:
            # Open file in write/binary.
            out_file = open(outfile, 'wb')
        except IOError:
            filecount += 1
            out_file = ''.join([filenm, str(filecount), fileext])

        for line in data.readlines():
            out_file.write(line)
        out_file.close()
        ui.notify(f"{outfile} was written")


def handle_upload(e: events.UploadEventArguments) -> None:
    """
    https://github.com/zauberzeug/nicegui/issues/585#issuecomment-1490738443

    :param e:
    :return:
    """
    with e.content as f:
        write_to_file(f, e.name)
        converted, coding = EncodeFile.detectfileencoding(e.name, 'utf-8')
        if not converted:
            filename = EncodeFile.encodefile(
                sourceFileName=e.name,
                sourceCoding=coding,
                targetCoding='utf-8'
            )
            os.remove(e.name)


@ui.page('/')
def index():
    global delete
    with ui.row():
        upload = ui.upload(on_upload=handle_upload).props('accept=.fhx').classes('max-w-full')

    with ui.row():
        ui.button('.fhx', on_click=pick_file, icon='folder')
        delete = ui.button('', icon='delete')
        delete.disable()
        ui.label().bind_text_from(_filename, 'filename')


ui.run(port=3001)