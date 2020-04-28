from .base import Action
from ..models import Member


class RequestPreferencesAction(Action):
    def execute(self, *, user_id: str, trigger_id: str):
        member = Member.objects.get(user_id=user_id)
        self.client.open_dialog(
            dialog={
                "callback_id": f"pref-{user_id}",
                "title": "Set Preferences",
                "submit_label": "Submit",
                "elements": [
                    {
                        "label": "Count",
                        "type": "select",
                        "hint": "Set how many times you'd like to be notified.",
                        "name": "coffee_count",
                        "placeholder": "Select a number...",
                        "value": member.coffee_count,
                        "options": [
                            {"label": "1", "value": "1"},
                            {"label": "2", "value": "2"},
                            {"label": "3", "value": "3"},
                            {"label": "4", "value": "4"},
                            {"label": "5", "value": "5"},
                        ],
                    },
                    {
                        "label": "Start Time",
                        "type": "select",
                        "hint": "Set the earliest time you'd like to be notified.",
                        "name": "start_time",
                        "placeholder": "Select a start time...",
                        "value": member.start_time.hour,
                        "options": [
                            {"label": "8am", "value": 8},
                            {"label": "9am", "value": 9},
                            {"label": "10am", "value": 10},
                            {"label": "11am", "value": 11},
                            {"label": "12pm", "value": 12},
                            {"label": "1pm", "value": 13},
                            {"label": "2pm", "value": 14},
                            {"label": "3pm", "value": 15},
                            {"label": "4pm", "value": 16},
                            {"label": "5pm", "value": 17},
                            {"label": "6pm", "value": 18},
                            {"label": "7pm", "value": 19},
                        ],
                    },
                    {
                        "label": "End Time",
                        "type": "select",
                        "hint": "Set the latest time you'd like to be notified.",
                        "name": "end_time",
                        "placeholder": "Select an end time...",
                        "value": member.end_time.hour,
                        "options": [
                            {"label": "8am", "value": 8},
                            {"label": "9am", "value": 9},
                            {"label": "10am", "value": 10},
                            {"label": "11am", "value": 11},
                            {"label": "12pm", "value": 12},
                            {"label": "1pm", "value": 13},
                            {"label": "2pm", "value": 14},
                            {"label": "3pm", "value": 15},
                            {"label": "4pm", "value": 16},
                            {"label": "5pm", "value": 17},
                            {"label": "6pm", "value": 18},
                            {"label": "7pm", "value": 19},
                        ],
                    },
                ],
            },
            trigger_id=trigger_id,
        )
