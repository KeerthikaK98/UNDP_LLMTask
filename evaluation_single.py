from langchain_community.llms import Ollama
from config import evaluation_model
import os

evaluator_llm = Ollama(model=evaluation_model)

def evaluate(question: str, answer: str, context: str) -> str:
    eval_prompt = f"""
You are a climate finance evaluation expert reviewing AI-generated answers.

Context:
{context}

Answer:
{answer}

Query: {question}

Evaluate the answers based on:
- Relevance (Does it directly address the query?)
- Accuracy (Is it fully supported by the context?)
- Clarity (Is it well-written and easy to understand?)

Respond in this format:
Relevance: High / Medium / Low
Accuracy: High / Medium / Low
Clarity: High / Medium / Low
Justification: [1–2 sentences]
"""
    try:
        response = evaluator_llm.invoke(eval_prompt)
        print("DEBUG: Raw response:\n", response)
        return response.strip() if isinstance(response, str) else str(response)
    except Exception as e:
        print("Error during LLM invocation:", e)
        return f"Error: {e}"

if __name__ == "__main__":
    question_s = "What barriers to climate finance implementation are identified in the documents?"
    answer_s = """The document identifies several barriers to climate finance implementation:

Macroeconomic challenges: Global economic volatility, driven by high inflation, rising interest rates, and geopolitical tensions, has created an unstable financial environment, particularly for developing countries. These nations are grappling with high levels of public debt, constrained fiscal space, and limited access to affordable financing.

Limited financing capacities: The financing capacities of many developed countries remain constrained by the economic shocks of the past decade, including the global financial crisis, COVID-19 pandemic, and sustained inflationary pressures. This has limited their ability to expand the scale of concessional finance and contributions to development assistance.

Fragmented international financial architecture: The fragmented international financial architecture, with insufficient alignment between climate finance mechanisms and development finance, hampers global efforts to meet the SDGs and respond effectively to the climate crisis. This fragmentation not only delays critical investments but also undermines the ability to scale up climate adaptation and mitigation efforts, particularly in the most vulnerable countries.

Unfavorable credit ratings: Developing countries face significant barriers in accessing finance due to unfavorable credit ratings linked to ongoing debt challenges.

Underdeveloped financial markets: Developing countries often have underdeveloped financial markets, which makes it difficult for them to tap into various financing sources.

Risk aversion: There is a risk aversion among investors and lenders when it comes to climate finance due to perceived higher risks associated with climate-related projects compared to traditional investments.

Lack of standardized frameworks: A lack of standardized frameworks for deploying innovative financing instruments at scale prevents countries from effectively utilizing these tools to enhance the efficiency of climate finance delivery.

Limited influence in global financial governance: Developing countries have limited influence in global financial governance, which hinders their ability to access and utilize climate finance efficiently.

To address these barriers, it is essential to strengthen global cooperation, implement systemic reforms to the global financial architecture, and encourage the use of innovative financial instruments that can help de-risk climate projects, attract private sector investment, and bridge the funding gap for SDG and climate investments. The Green Climate Fund is identified as a key player in this regard due to its unique mandate and capacity to catalyze co-investment in climate action in developing countries, especially the most vulnerable."""
    context_s = """Key barriers to climate finance implementation identified in the FFD4 and related climate policy documents include limited institutional capacity, especially in least developed and small island states, to access and manage international funding. Complex application processes, inconsistent eligibility requirements, and lengthy accreditation procedures hinder timely access to finance from multilateral funds like the Green Climate Fund (GCF) and Adaptation Fund.

A lack of harmonized data systems and transparent reporting frameworks makes it difficult to track climate finance flows and assess effectiveness. This also contributes to mistrust between donors and recipients. Another major barrier is the limited ability of local institutions to meet fiduciary and safeguard standards required by international funds.

Political instability, weak governance, and the absence of national climate finance strategies further reduce fund absorption capacity. Many developing countries also struggle with insufficient pipeline-ready projects due to a lack of technical expertise and feasibility assessments. Additionally, private investors face high perceived risks and unclear return profiles, making them reluctant to engage without public co-financing or guarantees.

The fragmentation of climate finance sources and a lack of coordination among donors exacerbate inefficiencies and result in overlapping or underfunded priorities.
"""
    result = evaluate(question_s, answer_s, context_s)
    print("\n Evaluation Result:\n", result)
