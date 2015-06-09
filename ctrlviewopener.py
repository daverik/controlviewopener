import sublime
import sublime_plugin
import os
from os import listdir
from os.path import isfile, join
import fnmatch


def splitext(path):
    for ext in ['.tar.gz', '.tar.bz2']:
        if path.endswith(ext):
            return path[:-len(ext)], path[-len(ext):]
    return os.path.splitext(path)


standardLayout = {
    "cols": [0.0, 1.0],
    "rows": [0.0, 1.0],
    "cells": [[0, 0, 1, 1]]
}


twoColumnLayout = {
    "cols": [0.0, 0.6, 1.0],
    "rows": [0.0, 1.0],
    "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
}

# Not used currently


def reorder_layout(view):
    window = view.window()
    if(window.num_groups() == 2):
        if len(window.views_in_group(2)) == 0:
            window.focus_group(1)
            window.set_layout(standardLayout)


class ExampleCommand(sublime_plugin.EventListener):

    def on_pre_close(self, view):
        if view is not None:
            window = view.window()
            name = os.path.basename(view.file_name())
            splittedText = splitext(name)
            if splittedText[1] == '.js':
                viewName = splittedText[0] + '.html'
                for v in view.window().views():
                    _name = os.path.basename(v.file_name())
                    if viewName == _name:
                        # reorder_layout(view)
                        v.close()

    def on_load(self, view):
        folders = view.window().folders()
        for folder in folders:
            for root, dirnames, filenames in os.walk(folder):
              for filename in fnmatch.filter(filenames, '*.js'):
                print(filename)
                print(folder)
            # matches.append(os.path.join(root, filename))
        name = os.path.basename(view.file_name())
        dirName = os.path.dirname(view.file_name())

        if splitext(name)[1] == '.js':
            view.window().set_view_index(view, 0, 0)
            view.window().focus_view(view)

            onlyfiles = [
                f for f in listdir(dirName) if isfile(join(dirName, f))]
            for f in onlyfiles:
                fileAndExtension = splitext(f)
                fileName = fileAndExtension[0]
                extensionName = fileAndExtension[1]
                if extensionName == '.html':
                    view.window().set_layout(twoColumnLayout)
                    viewView = view.window().open_file(dirName + '/' + f)
                    view.window().set_view_index(viewView, 1, 0)
                    view.window().focus_view(view)
