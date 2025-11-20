import openai
import pandas as pd
import time
from difflib import SequenceMatcher


openai.api_key = "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"  # ← Replace with your actual key

# Math problems with simplified expected answers
math_problems = [
    {"id": 1, "question": "What is the derivative of x^2?", "answer": "2x"},
    {"id": 2, "question": "Solve for x: x^2 + 4x + 4 = 0", "answer": "x=-2"},
    {"id": 3, "question": "If f(x) = 3x^3 - x, what is f''(2)?", "answer": "18"},
    {"id": 4, "question": "What is the integral of 1/x dx?", "answer": "ln|x| + C"},
    {"id": 5, "question": "Evaluate the limit: lim(x→0) sin(x)/x", "answer": "1"},
    {"id": 6, "question": "What is the derivative of sin(x)?", "answer": "cos(x)"},
    {"id": 7, "question": "Solve for x: 2x + 5 = 13", "answer": "x=4"},
    {"id": 8, "question": "What is the area of a circle with radius r?", "answer": "πr^2"},
    {"id": 9, "question": "If f(x) = x^2, what is f(3)?", "answer": "9"},
    {"id": 10, "question": "What is the slope of the line y = 4x - 7?", "answer": "4"},
]


# User profiles
user_profiles = {
    "novice": "User Level: Novice",
    "intermediate": "User Level: Intermediate",
    "expert": "User Level: Expert"
}

# Improved prompt creator
def generate_prompt(style, profile, question):
    if style == "no_cot":
        return f"Answer this question directly: {question}"
    elif style == "auto_cot":
        return f"Think step by step to solve this math problem: {question}"
    elif style == "personalized":
        if profile == "novice":
            return f"Explain to a beginner with limited math knowledge: {question}"
        elif profile == "intermediate":
            return f"Explain to someone with basic calculus knowledge: {question}"
        else:  # expert
            return f"Provide an advanced mathematical explanation for: {question}"

def get_response(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Improved evaluation function
def evaluate_response(response, expected_answer, prompt):
    # Check if the core answer is present (more flexible matching)
    # Extract key parts from expected_answer and check if they appear in response
    key_parts = expected_answer.replace(" ", "").lower()
    clean_response = response.replace(" ", "").lower()
    
    # For derivative or equations, look for the core answer
    correct = key_parts in clean_response
    
    # Coherence: Based on response length and structure
    coherence = 3
    if len(response.split()) > 15:  # Has some explanation
        coherence += 1
    if "step" in response.lower():  # Shows step-by-step reasoning
        coherence += 1
        
    # Personalization: Check if response style matches user level
    personalization = 2
    profile_level = "novice" if "novice" in prompt.lower() else "intermediate" if "intermediate" in prompt.lower() else "expert"
    
    # For novice: Check for simpler explanations
    if profile_level == "novice" and ("basic" in response.lower() or "simple" in response.lower()):
        personalization += 2
    # For expert: Check for advanced terminology
    elif profile_level == "expert" and any(term in response.lower() for term in ["calculus", "function", "differential"]):
        personalization += 2
    # For intermediate: Check for moderate detail
    elif profile_level == "intermediate" and not any(term in response.lower() for term in ["basic", "simple"]) and len(response.split()) > 30:
        personalization += 2
        
    return correct, coherence, personalization

# Custom function to print a nice table
def print_table(data, headers, title=None):
    # Calculate column widths based on content
    col_widths = [max(len(str(row[i])) for row in data + [headers]) + 2 for i in range(len(headers))]
    
    # Calculate total table width
    total_width = sum(col_widths) + len(col_widths) + 1
    
    if title:
        print("\n" + "=" * total_width)
        print(title.center(total_width))
        print("=" * total_width)
    
    print("+" + "+".join("-" * width for width in col_widths) + "+")
    header_row = "|"
    for i, header in enumerate(headers):
        header_row += str(header).center(col_widths[i]) + "|"
    print(header_row)
    print("+" + "+".join("-" * width for width in col_widths) + "+")
    
    for row in data:
        data_row = "|"
        for i, cell in enumerate(row):
            if isinstance(cell, float):
                data_row += f"{cell:.2f}".center(col_widths[i]) + "|"
            else:
                data_row += str(cell).center(col_widths[i]) + "|"
        print(data_row)
    
    print("+" + "+".join("-" * width for width in col_widths) + "+")

# Function to print organized results during run
def print_test_result(style, profile, question, response, expected, correct, coherence, personalization):
    border = "=" * 60
    print(f"\n{border}")
    print(f"TEST: {style.upper()} / {profile.upper()}")
    print(border)
    print(f"Q: {question}")
    print("-" * 60)
    print(f"Response:\n{response}")
    print("-" * 60)
    print(f"Expected answer: {expected}")
    print(f"Correct: {'Yes' if correct else 'No'}")
    print(f"Coherence score: {coherence}/5")
    print(f"Personalization score: {personalization}/4")

# Experiment run
results = []
for prob in math_problems:
    for profile in ["novice", "intermediate", "expert"]:
        for style in ["no_cot", "auto_cot", "personalized"]:
            prompt = generate_prompt(style, profile, prob["question"])
            response = get_response(prompt)
            correct, coherence, personalization = evaluate_response(response, prob["answer"], prompt)
            
            # Print organized result
            print_test_result(
                style, profile, prob["question"], response, 
                prob["answer"], correct, coherence, personalization
            )
            
            results.append({
                "problem_id": prob["id"],
                "problem": prob["question"],
                "profile": profile,
                "style": style,
                "prompt": prompt,
                "response": response,
                "expected": prob["answer"],
                "accuracy": int(correct),
                "coherence_score": coherence,
                "personalization_score": personalization
            })
            
            time.sleep(1.5)

# Save results
df = pd.DataFrame(results)
df.to_csv("openai_auto_cot_results.csv", index=False)

# Print summary results
print("\n\n" + "=" * 80)
print("EXPERIMENT RESULTS SUMMARY".center(80))
print("=" * 80)

# 1. Style summary
style_summary = df.groupby("style")[["accuracy", "coherence_score", "personalization_score"]].mean().reset_index()
style_data = []
for _, row in style_summary.iterrows():
    style_data.append([row["style"], row["accuracy"], row["coherence_score"], row["personalization_score"]])
print_table(style_data, ["Style", "Accuracy", "Coherence", "Personalization"], "1. PERFORMANCE BY PROMPTING STYLE")

# 2. Profile summary
profile_summary = df.groupby("profile")[["accuracy", "coherence_score", "personalization_score"]].mean().reset_index()
profile_data = []
for _, row in profile_summary.iterrows():
    profile_data.append([row["profile"], row["accuracy"], row["coherence_score"], row["personalization_score"]])
print_table(profile_data, ["Profile", "Accuracy", "Coherence", "Personalization"], "2. PERFORMANCE BY USER PROFILE")

# 3. Combined summary
combined_summary = df.groupby(["style", "profile"])[["accuracy", "coherence_score", "personalization_score"]].mean().reset_index()
combined_data = []
for _, row in combined_summary.iterrows():
    combined_data.append([row["style"], row["profile"], row["accuracy"], row["coherence_score"], row["personalization_score"]])
print_table(combined_data, ["Style", "Profile", "Accuracy", "Coherence", "Personalization"], "3. DETAILED PERFORMANCE BY STYLE AND PROFILE")

# 4. Problem summary
problem_summary = df.groupby(["problem_id", "problem"])[["accuracy", "coherence_score", "personalization_score"]].mean().reset_index()
problem_data = []
for _, row in problem_summary.iterrows():
    problem_data.append([row["problem_id"], row["problem"], row["accuracy"], row["coherence_score"], row["personalization_score"]])
print_table(problem_data, ["ID", "Problem", "Accuracy", "Coherence", "Personalization"], "4. PERFORMANCE BY PROBLEM")

print("\n" + "=" * 80)
print("EXPERIMENT COMPLETED SUCCESSFULLY".center(80))
print("=" * 80)