from box import Box
from src.util import csv_open_as_json, grouper


def get_stories():
    id_col = "MV Number - Based on Word count (S - L)"
    stories = [d for d in csv_open_as_json("data/lav/stories.csv") if d.get("Story", "") != ""]
    assert len(stories) == len(set([d[id_col] for d in stories]))
    # Additionally name for id_col
    for d in stories:
        d["id"] = d[id_col]
        d["engine"] = "human"
    return stories


def get_questions():
    questions = [
        1,
        "Emotional Intensity",
        "How emotionally intense was this event?",
        "1 = Not at all emotionally intense",
        "7 = Extremely emotionally intense",

        2,
        "Emotion Aversion",
        "How emotionally unpleasant was this event?",
        "1 = Not at all aversive or unpleasant",
        "7 = Extremely aversive or unpleasant",

        3,
        "Harm",
        "How much harm did this action do to others?",
        "1 = No harm to others",
        "7 = Extreme harm to others",

        4,
        "Self Benefit",
        "How much did this action benefit the main actor (YOU)?",
        "1 = No benefit to main actor (YOU)",
        "7 = Extreme benefit to main actor (YOU)",

        5,
        "Other Benefit",
        "How much did this action benefit others?",
        "1 = No benefit for others",
        "7 = Extreme benefit for others",

        6,
        "Pre-meditated",
        "How much planning went into this action?",
        "1 = The action was completely unplanned",
        "7 =The action was completely planned",

        7,
        "Illegality",
        "How legal was this action?",
        "1 = The action was extremely illegal",
        "7 = The action was extremely legal",

        8,
        "Social Norm Violation",
        "Does this action follow social rules?",
        "1 = This action breaks social rules",
        "7 = This action follows social rules",

        9,
        "Socialness",
        "Are other people involved in this action?",
        "1 = No other people are involved in the action",
        "7 = Other people are extremely involved in the action",

        10,
        "Frequency",
        "How often do you think this type of event actually happens?",
        "1 = This type of event rarely occurs",
        "7 = This type of event occurs all the time",

        11,
        "Personal Familiarity",
        "Have you ever experienced this type of event?",
        "1 = Never experienced this type of event",
        "7 = Frequently experienced this type of event",

        12,
        "General Familiarity",
        "Have you thought about this type of event?",
        "1 = Never thought about this type of event",
        "7 = Frequently think about this type of event",

        13,
        "Morally Appropriate",
        "Was this action morally appropriate?",
        "1 = Extremely morally inappropriate",
        "7 = Extremely morally appropriate",

        14,
        "Self Harm",
        "How much harm did this action do to the main actor (YOU)?",
        "1 = No self-harm towards main actor (YOU)",
        "7 = Extreme self-harm towards main actor (YOU)",

        15,
        "Personal Frequency",
        "Was this action a one-time event or something that the main actor (YOU) did frequently?",
        "1 = One-time event",
        "7 = Frequently",

        # TODO change 'main actor (YOU)' in all of these to 'you'
        16,
        "Acted Differently",
        "How likely is it that the main actor (YOU) would have acted differently in this specific event?",
        "1 = Extremely unlikely",
        "7 = Extremely likely",
    ]

    return {
        m: Box(id=iid, measure=m, question=q, high=h, low=l)
        for iid, m, q, h, l in list(grouper(questions, 5))
    }
