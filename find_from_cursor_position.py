import sublime
import sublime_plugin


class FindFromCursorPosition(sublime_plugin.TextCommand):

    @property
    def highlighted_regions(self):
        result = []
        for i in range(100):
            region = self.view.get_regions('highlight_word_{}'.format(i))
            if not region:
                break
            result.append(region)
        return result

    def run(self, edit, find_next=True):
        for region in self.view.sel():
            if region.empty():
                region = self.view.word(region)
            break

        for word_regions in self.highlighted_regions:
            for i, selection_region in enumerate(word_regions):
                if selection_region.contains(region):
                    search_word = self.view.substr(selection_region)
                    offset = 1 if find_next else -1
                    region = word_regions[(i + offset) % len(word_regions)]
                    self.view.sel().clear()
                    self.view.sel().add(region)
                    sublime.status_message(search_word)
                    return

        self.view.sel().clear()
        self.view.sel().add(region)
        self.view.window().run_command('slurp_find_string')
        self.view.window().run_command('show_panel', {'panel': 'find', 'toggle': False})
        if find_next:
            self.view.window().run_command('find_next')
        else:
            self.view.window().run_command('find_prev')
