import uiautomation as auto


class ContextService:
    def __init__(self, context_word=3):
        self.context_word=context_word
    def get_context(self):
        focused_control = auto.GetFocusedControl()
        if not focused_control:
            return None
        text_pattern = focused_control.GetPattern(auto.PatternId.TextPattern)
        if not text_pattern:
            return None
        selection=text_pattern.GetSelection()
        if not selection:
            return None
        selected_range = selection[0]
        selected_text = selected_range.GetText(-1).strip()
        if not selected_text:
            return None
        before_range = selected_range.Clone()
        after_range = selected_range.Clone()
        before_range.MoveEndpointByUnit(
            auto.TextPatternRangeEndpoint.Start,
            auto.TextUnit.Word,
            -self.context_word
        )

        before_range.MoveEndpointByRange(
            auto.TextPatternRangeEndpoint.End,
            selected_range,
            auto.TextPatternRangeEndpoint.Start
        )


        after_range.MoveEndpointByUnit(
            auto.TextPatternRangeEndpoint.End,
            auto.TextUnit.Word,
            self.context_word
        )
        
        after_range.MoveEndpointByRange(
            auto.TextPatternRangeEndpoint.Start,
            selected_range,
            auto.TextPatternRangeEndpoint.End
        )

        
        before_text=before_range.GetText(-1).strip()
        after_text=after_range.GetText(-1).strip()
        return{"before":before_text, "selected":selected_text, "after":after_text}
    