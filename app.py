import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

# Page configuration for a clean, academic look
st.set_page_config(page_title="Formulaic Mindset Scale", page_icon="🧠", layout="centered")

st.title("🧠 Formulaic Mindset Scale")
st.markdown("""
Find out where you stand on the **Formulaic Mindset Scale (FMS-15)** compared to our research sample of university students ($N=196$)!
""")
st.write("---")

# The 15 Items validated from your EFA
factor1_items = [
    "I often get stuck when there is more than one correct option.",
    "I believe that not following the model answer closely may lead to negative outcomes.",
    "I would rather follow an established method, even when I’m not sure if it will definitely work.",
    "If I make a mistake, I review the exact steps to see where I deviated from the established method.",
    "I often try to apply a standard formula to a problem, even if it doesn't fit perfectly.",
    "I feel more secure when copying methods that have been successful instead of trying something new.",
    "I tend to delay starting tasks if the correct approach is not clear.",
    "I feel uneasy when a task doesn’t have a clear, single correct answer.",
    "I find it difficult to deviate from established methods when the stakes are high."
]

factor2_items = [
    "I prefer figuring things out through trial and error rather than following established methods.",
    "I usually don't need to compare my work to a model answer to feel confident.",
    "I am comfortable developing my own methods without relying on set formulas.",
    "I believe that success often depends on factors other than following the correct method.",
    "I enjoy tasks that can be solved in multiple ways rather than having only one correct way.",
    "I believe it is important to search for multiple solutions, even when a correct method is already known."
]

# Create a master list of dictionaries tracking item properties
all_items = []
for i, text in enumerate(factor1_items):
    all_items.append({"text": text, "factor": 1, "index": i})
for i, text in enumerate(factor2_items):
    all_items.append({"text": text, "factor": 2, "index": i})

# Jumble the items deterministically so they are mixed but stable across app refreshes
np.random.seed(42)
np.random.shuffle(all_items)

st.subheader("Respond to the statements below:")

# Visual callout box to make the response scale highly obvious
st.info("""
**Response Scale Reference:**
* **1** = Not at all characteristic of me
* **2** = Slightly characteristic of me
* **3** = Moderately characteristic of me
* **4** = Very characteristic of me
* **5** = Entirely characteristic of me
""")

# Render all jumbled items sequentially and collect user inputs
ui_responses = {}
for display_idx, item in enumerate(all_items):
    unique_key = f"f{item['factor']}_{item['index']}"
    
    score = st.slider(
        f"Q{display_idx + 1}: {item['text']}", 
        1, 5, 3, 
        key=unique_key
    )
    
    if item['factor'] == 1:
        ui_responses[f"f1_{item['index']}"] = score
    else:
        ui_responses[f"f2_{item['index']}"] = score

st.write("---")

# Scoring and Data Analysis Display
if st.button("Calculate My Profile", type="primary"):
    # Capture timestamp of response entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Factor 1: Direct scoring
    user_f1 = sum([ui_responses[f"f1_{i}"] for i in range(len(factor1_items))])
    
    # Factor 2: Reverse-scoring calculation (6 - raw_score)
    user_f2 = sum([(6 - ui_responses[f"f2_{i}"]) for i in range(len(factor2_items))])
    
    # Validation Sample Data Constants
    m1, sd1 = 28.4, 4.2  
    m2, sd2 = 18.2, 3.5  
    total_mean = m1 + m2
    total_sd = np.sqrt(sd1**2 + sd2**2)
    user_total = user_f1 + user_f2
    
    st.subheader("🎯 Your Metrics vs. Student Cohort")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Model-Based Belief Score", value=user_f1, delta=f"{user_f1 - m1:+.1f} vs Avg")
        st.caption(f"Cohort Average: {m1} (Max Score: 45)")
    with col2:
        st.metric(label="Procedural Rigidity Score", value=user_f2, delta=f"{user_f2 - m2:+.1f} vs Avg")
        st.caption(f"Cohort Average: {m2} (Max Score: 30)")
        
    st.write("")
    
    # --- PSYCHOMETRIC INTERPRETATION SECTION (Uniform 0.5 SD Threshold) ---
    st.markdown("### 🔍 Profile Interpretation")
    
    # Factor 1: Model-Based Belief Interpretation
    if user_f1 > (m1 + 0.5 * sd1):
        f1_interpret = "Relatively Higher. You hold a strong core conviction that single, 'correct' model answers exist. You rely heavily on external benchmarks for guidance and derive your task confidence primarily from verified templates."
    elif user_f1 < (m1 - 0.5 * sd1):
        f1_interpret = "Relatively Lower. You display a weak reliance on external benchmarks. You are comfortable operating without model answers or pre-existing templates to guide your confidence."
    else:
        f1_interpret = "Moderate. You display a balanced profile. You appreciate external benchmarks and clear models for reassurance, but your confidence isn't entirely dependent on them."

    # Factor 2: Procedural Rigidity Interpretation
    if user_f2 > (m2 + 0.5 * sd2):
        f2_interpret = "Relatively Higher. You experience significant cognitive discomfort with trial-and-error processes. You show a distinct reluctance to explore multiple paths or alternative solutions when an established method is already available."
    elif user_f2 < (m2 - 0.5 * sd2):
        f2_interpret = "Relatively Lower. You are highly adaptable. You lean comfortably into trial-and-error and enjoy actively exploring multiple diverse solutions, even when an established path exists."
    else:
        f2_interpret = "Moderate. You are generally comfortable following standard operating guidelines but remain reasonably open to troubleshooting via trial-and-error if a task requires it."

    st.markdown(f"**Factor 1: Model-Based Belief**\n> {f1_interpret}")
    st.markdown(f"**Factor 2: Procedural Rigidity**\n> {f2_interpret}")
    
    st.write("")
    st.markdown("### Distribution Trajectory")
    
    # Plotting User Score on Population Distribution Density Curve
    fig, ax = plt.subplots(figsize=(7, 3.2))
    
    np.random.seed(42)
    simulated_population = np.random.normal(total_mean, total_sd, 1000)
    sns.kdeplot(simulated_population, fill=True, color="#ffde77", alpha=0.5, ax=ax, label="Singaporean Sample ($N=196$)")
    
    ax.axvline(user_total, color="#1d4263", linestyle="--", linewidth=2.5, label=f"Your Total Score ({user_total})")
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_xlabel("Cumulative Formulaic Mindset Index")
    ax.legend(frameon=False, loc="upper left")
    
    st.pyplot(fig)
    
    # --- GLOBAL POSITIONING INTERPRETATION (Below the Graph) ---
    st.write("")
    if user_total > (total_mean + 0.5 * total_sd):
        trajectory_text = f"On average, your overall mindset score is **above average** as compared to our Singaporean sample. This suggests a more pronounced preference for structure, external models, and methodical certainty than the average university peer."
    elif user_total < (total_mean - 0.5 * total_sd):
        trajectory_text = f"On average, your overall mindset score is **below average** as compared to our Singaporean sample. This indicates you lean significantly more toward cognitive flexibility, organic exploration, and comfort with unscripted tasks than your typical peers."
    else:
        trajectory_text = f"On average, your overall mindset score is **around average** as compared to our Singaporean sample. Your baseline cognitive style aligns closely with the central trends of the local university cohort, balancing structured methods with baseline adaptive problem-solving."
        
    st.success(trajectory_text)
    
    # --- DATA EXPORT PROCESSING ---
    row_data = {
        "Timestamp": [timestamp],
        "Total_Score": [user_total],
        "Factor1_Score": [user_f1],
        "Factor2_Score": [user_f2]
    }
    for display_idx, item in enumerate(all_items):
        key = f"f{item['factor']}_{item['index']}"
        row_data[f"Q{display_idx + 1}_Raw"] = [ui_responses[key]]
        
    export_df = pd.DataFrame(row_data)
    
    st.write("")
    st.download_button(
        label="📥 Download My Scale Response Metadata (.csv)",
        data=export_df.to_csv(index=False).encode('utf-8'),
        file_name=f"FMS_Scale_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    # --- NEW CLOSING REMARKS CALLOUT ---
    st.write("")
    st.info("""
    ✨ **Thank you for participating!** We hope you had fun taking this little test. While our pilot sample size comparisons are currently small ($N=196$), this is definitely a meaningful first step toward a larger psychological framework we are actively developing. We hope to continue expanding our findings and look forward to refining this scale further!
    """)