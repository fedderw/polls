import ubicenter
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from py import preprocess_data as ppd

VARIABLE_MAPPING = {
    "Poll ID": "poll_id",
    "Question ID": "question_id",
    "Cross-tab variable 1": "xtab1_var",
    "Cross-tab value 1": "xtab1_val",
    "Cross-tab variable 2": "xtab2_var",
    "Cross-tab value 2": "xtab2_val",
    "Sample size": "sample_size",
    "Question text": "question_text",
    "Percentage": "pct",
    "Response": "response",
    "Favorability": "favorability",
    "Date": "date",
    "Pollster": "pollster",
    "Notes": "notes",
}

variable_mapping_inverse = {v: k for k, v in VARIABLE_MAPPING.items()}
variable_mapping_inverse["question_text_wrap"] = "Question"
variable_mapping_inverse["pollster_wrap"] = "Pollster"
variable_mapping_inverse["pct_fav"] = "% favorability"


def poll_vis(responses, poll_id, question_id=None, crosstab_var_1="-",crosstab_var_2="-"):
    """[summary]

    Parameters
    ----------
    responses : [type]
        [description]
    poll_id : [type]
        [description]
    question_id : [type], optional
        [description], by default None
    crosstab_var_1 : str, optional
        [description], by default "-"
    """
    # return none if no poll_id
    # this messes up the rest of the poll_vis function for some reason
    # if poll_id == None:
    #     return None
    if question_id is None:
        target_questions = responses[responses.poll_id == poll_id].question_id.unique()
        # check if there's only one question for the poll, if there's more than 1 --
        # tell the user that's not supported
        assert target_questions.size == 1, "Please select a question:"
        # + target_questions -- have the assert statement include a list of the question options
        question_id = target_questions[0]
    target_responses = responses[
        (responses.poll_id == poll_id)
        & (responses.question_id == question_id)
        & (responses.xtab1_var == crosstab_var_1)
    ]
    
    nunique_xtab1_vars=len(target_questions.xtab1_var.unique())
    target_responses["question_text_wrap"] = ppd.plotly_wrap(target_responses.question_text.copy(),130)
    # question_text=target_responses["question_text_wrap"].iloc[0] 
    question_text=target_responses["question_text_wrap"].unique()[0] if target_responses.shape[0] > 0 else "No question text"
    
    if crosstab_var_1 == "-" & nunique_xtab1_vars > 1:
        fig = make_subplots(
            rows=nunique_xtab1_vars, cols=1, shared_xaxes=True, subplot_titles=target_questions.xtab1_var.unique()
            )
        
        for i, var in enumerate(target_questions.xtab1_var.unique()):
            fig.add_trace(
                px.bar(
                    target_responses[target_responses.xtab1_var == var],
                    x="xtab1_val",
                    y="response",
                    text=target_responses.question_text_wrap,
                    textposition="auto",
                    name=var,
                    marker={"color": "black"},
                    opacity=0.8,
                ),
                row=i + 1,
                col=1,
            )
        
        fig.update_layout(
        xaxis_title="Percentage", yaxis_title=crosstab_var_1, xaxis_tickformat="%",
        )
        
        return fig
    
    else:
        # if cross tabs, pull the corresponding responses, but if no crosstabs selected, pull the response
        # from the "-" rows
        fig = px.bar(
            target_responses,
            x="percent_norm",
            y="xtab1_val",
            color="response",
            barmode="stack",
            orientation="h",
            title=question_text,
        )
        fig.update_layout(
            xaxis_title="Percentage", yaxis_title=crosstab_var_1, xaxis_tickformat="%",
        )
    return fig

# Function to create a bubble chart for % favorability across a set of poll/question pairs.
def bubble_chart(
    responses, poll_ids=None, question_ids=None, xtab1_var="-", xtab1_val="-"
):
    """[summary]

    Parameters
    ----------
    responses : [type]
        [description]
    poll_ids : [type], optional
        [description], by default None
    question_ids : [type], optional
        [description], by default None
    xtab1_var : str, optional
        [description], by default "-"
    xtab1_val : str, optional
        [description], by default "-"
    """
    # TODO (ideas):
    # 1) Add the line to zero for a "stem" chart (also add a zero hline)
    # 2) xtab2_var and xtab2_val
    # 3) Formal function docstring.
    # 4) Set color palettes for ordinal xtabs (also something for gender?)
    # Subset the data per the specifications.
    target_data = responses[responses.xtab1_var == xtab1_var]
    # Only subset by xtab1_val if we're not splitting by it.
    xtab_split = (xtab1_var != "-") & (xtab1_val == "-")
    if not xtab_split:
        target_data = target_data[target_data.xtab1_val == xtab1_val]
    # Summarize to the poll/question level.
    GROUPBY = [
        "poll_id",
        "question_id",
        "question_text_wrap",
        "date",
        "pollster_wrap",
        "sample_size",
    ]
    if xtab_split:
        GROUPBY += ["xtab1_val"]
    poll_question = target_data.groupby(GROUPBY).pct_fav.sum().reset_index()
    if poll_ids is not None:
        poll_question = poll_question[poll_question.poll_id.isin(poll_ids)]
    if question_ids is not None:
        poll_question = poll_question[poll_question.question_id.isin(question_ids)]
    # return poll_question
    # Visualize as a scatter chart.
    if xtab_split:
        variable_mapping_inverse_tmp = variable_mapping_inverse.copy()
        variable_mapping_inverse_tmp["xtab1_val"] = xtab1_var
        fig = px.scatter(
            poll_question,
            x="date",
            y="pct_fav",
            color="xtab1_val",
            text="pollster_wrap",
            size="sample_size",
            hover_data=["question_text_wrap"],
            labels=variable_mapping_inverse_tmp,
        )
    else:
        fig = px.scatter(
            poll_question,
            x="date",
            y="pct_fav",
            text="pollster_wrap",
            size="sample_size",
            hover_data=["question_text_wrap"],
            labels=variable_mapping_inverse,
        )
    return ubicenter.format_fig(show=False)
