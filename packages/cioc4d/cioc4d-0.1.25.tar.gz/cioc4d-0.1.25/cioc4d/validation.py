import abc
import importlib
import inspect
import os
import re
import c4d
from ciocore.expander import Expander
from cioc4d import asset_cache
from ciocore.gpath import Path
from ciocore.gpath_list import GLOBBABLE_REGEX, PathList
from ciocore.validator import Validator, ValidationError


class ValidateUploadDaemon(Validator):
    def run(self, _):
        dialog = self._submitter
        use_daemon = dialog.section(
            "UploadOptionsSection").use_daemon_widget.get_value()
        if not use_daemon:
            return

        msg = "This submission expects an uploader daemon to be running.\n After you press submit you can open a shell and type: 'conductor uploader'"

        location = (dialog.section(
            "LocationSection").widget.get_value() or "").strip()
        if location:
            msg = "This submission expects an uploader daemon to be running and set to a specific location tag.\nAfter you press OK you can open a shell and type: 'conductor uploader --location {}'".format(
                location)

        self.add_notice(msg)
        # By also writing the message to the console, the user can copy paste
        # `conductor uploader --location blah`.
        c4d.WriteConsole(msg)


class ValidateTaskCount(Validator):
    def run(self, _):
        dialog = self._submitter
        count = dialog.section("InfoSection").frame_count
        if count > 1000:
            self.add_notice(
                "This submission contains over 1000 tasks ({}). Are you sure this is correct?".format(count))


class ValidateDestinationDirectoryClash(Validator):
    def run(self, _):
        dialog = self._submitter
        context = dialog.get_context()
        expander = Expander(safe=True, **context)
        dest = expander.evaluate(dialog.section(
            "GeneralSection").destination_widget.get_value())

        dest_path = Path(dest).posix_path(with_drive=False)
        # print "dest_path:" dest_path

        for gpath in asset_cache.data(self._submitter):
            asset_path = gpath.posix_path(with_drive=False)
            if asset_path.startswith(dest_path):
                c4d.WriteConsole("Some of your upload assets exist in the specified output destination directory\n. {} contains {}".format(
                    dest_path, asset_path))
                self.add_error(
                    "The destination directory for rendered output contains assets that are in the upload list. This can cause your render to fail. See the script editor for details.")
                break
            if dest_path.startswith(asset_path):
                c4d.WriteConsole("You are trying to upload a directory that contains your destination directory.\n. {} contains {}".format(
                    asset_path, dest_path))
                self.add_error(
                    "One of your assets is a directory that contains the specified output destination directory. This will cause your render to fail. See the script editor for details.")
                break


class ValidateRenderToDestinationDirectory(Validator):
    def run(self, _):
        dialog = self._submitter
        context = dialog.get_context()
        expander = Expander(safe=True, **context)
        dest = expander.evaluate(dialog.section(
            "GeneralSection").destination_widget.get_value())
        dest_path = Path(dest).posix_path(with_drive=False)

        task_template = dialog.section("TaskSection").widget.get_value()
        overrides_image = "-oimage" in task_template
        overrides_multipass = "-omultipass" in task_template

        document = c4d.documents.GetActiveDocument()
        render_data = document.GetActiveRenderData()

        save_enabled = render_data[c4d.RDATA_GLOBALSAVE]

        if not save_enabled:
            self.add_warning(
                "Saving images is not enabled in Render settings. Your render will most likely fail.")

        do_image_save = render_data[c4d.RDATA_SAVEIMAGE]
        do_multipass_save = render_data[c4d.RDATA_MULTIPASS_SAVEIMAGE] and render_data[c4d.RDATA_MULTIPASS_ENABLE]

        if overrides_image:
            self.add_notice(
                "Your task template overrides the Render Settings image path with the '-oimage' flag. This is fine, but please ensure it points to a writable directory on Conductor's render node. It should be somewhere below the Destination Directory as specified in the general section of the Conductor dialog.")
        elif do_image_save:
            try:
                image_path = Path(render_data[c4d.RDATA_PATH]).posix_path(
                    with_drive=False)

                if not image_path.startswith(dest_path):
                    self.add_warning(
                        "The image path you've set in Render Settings does not point to a writable location. If you continue, your submission will probably fail. Images should be written somewhere below the Destination Directory as specified in the general section of the Conductor dialog. You should change either the path in Render Settings, or the Conductor destination directory.")
            except ValueError:
                self.add_warning(
                    "The image path you've set in Render Settings is not a valid path. If you continue, your submission will probably fail. Images should be written somewhere below the Destination Directory as specified in the general section of the Conductor dialog. You should change either the path in Render Settings, or the Conductor destination directory.")
        else:
            self.add_notice(
                "This file does not specify a single-pass output image.")

        if overrides_multipass:
            self.add_notice(
                "Your task template overrides the Render Settings multipass image path with the '-omultipass' flag. This is fine, but please ensure it points to a writable directory on Conductor's render node. It should be somewhere below the Destination Directory as specified in the general section of the Conductor dialog.")
        elif do_multipass_save:
            try:
                multipass_path = Path(
                    render_data[c4d.RDATA_MULTIPASS_FILENAME]).posix_path(with_drive=False)

                if not multipass_path.startswith(dest_path):
                    self.add_warning("The multipass image path you've set in Render Settings does not point to a writable location. If you continue, you will not be able to download your multipass images. Images should be written somewhere below the Destination Directory as specified in the general section of the Conductor dialog. You should change either the multipass path in Render Settings, or the Conductor destination directory.")
            except ValueError:
                self.add_warning(
                    "The multipass path you've set in Render Settings is not a valid path. If you continue, your submission will probably fail. Images should be written somewhere below the Destination Directory as specified in the general section of the Conductor dialog. You should change either the path in Render Settings, or the Conductor destination directory.")
        else:
            pass
            # The notice below seems pointless because multipass is (probably) not a normal thing in c4d.
            # self.add_notice("This file does not specify a multipass output image.")


class ValidateMissingExtraAssets(Validator):

    def run(self, _):

        missing = []
        for gpath in self._submitter.section("AssetsSection").pathlist:
            pp = gpath.posix_path()
            if not os.path.exists(pp):
                missing.append(pp)

        if missing:
            self.add_warning(
                "Some of the assets specified in the Extra Assets section do not exist on disk. See the console for details. You can continue if you don't need them.")

            c4d.WriteConsole("----- Conductor Asset Validation -------\n")
            for asset in missing:
                c4d.WriteConsole("Missing: {}\n".format(asset))


# Implement more validators here
####################################
####################################


def run(dialog, submitting=True):

    errors, warnings, notices = _run_validators(dialog)

    if errors:
        msg = ""
        msg += "Some errors would cause the submission to fail:\n\n" + \
            "\n".join(errors)+"\n"
        c4d.gui.MessageDialog(msg,  type=c4d.GEMB_OK)
        raise ValidationError(msg)
    if notices or warnings:
        if submitting:
            msg = "Would you like to continue this submission?\n\n"
            dialog_type = c4d.GEMB_OKCANCEL
        else:
            msg = "Validate only.\n\n"
            dialog_type = c4d.GEMB_OK

        if warnings:
            msg += "Please check the warnings below:\n\n" + \
                "\n\n".join(["[WARN]:{}".format(w) for w in warnings]) + "\n\n"
        if notices:
            msg += "Please check the notices below:\n\n" + \
                "\n\n".join(["[INFO]:{}".format(n) for n in notices]) + "\n\n"

        result = c4d.gui.MessageDialog(msg, type=dialog_type)
        if result != c4d.GEMB_R_OK:
            c4d.WriteConsole("Submission cancelled by user.\n")
            raise ValidationError(msg)
    # Either there were no  messages, or the user clicked Continue (OK)


def _run_validators(dialog):
    # Eventually we will handle takes here
    takename = "Main"
    validators = [plugin(dialog) for plugin in Validator.plugins()]
    for validator in validators:
        validator.run(takename)

    errors = list(set.union(*[validator.errors for validator in validators]))
    warnings = list(
        set.union(*[validator.warnings for validator in validators]))
    notices = list(set.union(*[validator.notices for validator in validators]))
    return errors, warnings, notices
