# Questioning Guide

This guide describes how to gather requirements from users before delegating work to specialists.

## Question Phases

### Phase 1: Intent (Always Required)

Always start by understanding what the user wants to accomplish.

**Basic Intent Questions:**
- What are you trying to accomplish?

**With Success Criteria:**
- What are you trying to accomplish?
- How will you know this is done successfully?

These questions help you understand the goal and what completion looks like.

### Phase 2: Scope (When Needed)

Ask scope questions when the boundaries of the work are unclear.

**File or Component Scope:**
- Which files or components should we work with?

**Integration Approach:**
- How should this integrate with existing code?
  - Create new component
  - Extend existing code
  - Replace current implementation

**Implementation Preferences:**
- Any preferences for implementation approach?
  - Quick and simple (fast, minimal)
  - Comprehensive (thorough with tests and documentation)

### Phase 3: Confirmation (Always Required)

Always confirm your understanding before proceeding.

**Simple Confirmation:**
Summarize the plan and ask:
- I will [plan summary]. Should I proceed?
  - Yes, go ahead
  - No, ask more questions

**Detailed Confirmation:**
For complex plans, break it down:
- Based on our discussion, I will:
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
  
  Does this look correct?
  - Yes, proceed with this plan
  - Adjust the plan (I want to modify something)

## Best Practices

### Batch Related Questions
Group 2-4 related questions together rather than asking one at a time. This keeps the conversation efficient while gathering complete context.

**Example of batched questions:**
- What are you trying to accomplish?
- What does success look like?
- Which components should we focus on?
- Any constraints or preferences?

### Explain Trade-offs
When offering options, explain the implications:
- Quick and simple: Faster to implement but may need refinement later
- Comprehensive: Takes longer initially but more robust

### Always Get Confirmation
Never proceed to delegation without explicit confirmation. The user should agree to your understanding of the plan.

### Continue Until Clear
Keep asking questions until you have enough context to:
- Identify which specialists to involve
- Write clear natural language instructions
- Specify deliverables and success criteria

## Question Structure

Each question should have:

1. **Header** - Short label (1-2 words) that categorizes the question
2. **Question text** - Clear, specific question
3. **Options** (when applicable) - Predefined choices with descriptions
   - For open-ended questions, leave options empty
   - For multiple choice, provide clear labels and explanations

## Examples by Scenario

### Creating a New Agent

**Intent:**
- What should this agent do?
- How will you know it's working correctly?

**Scope:**
- What tools should the agent use?
- Where should I save the configuration?
- Any specific naming preferences?

**Confirmation:**
- I will create a [type] agent that does [function], using [tools], and save to [location]. Should I proceed?

### Debugging an Issue

**Intent:**
- What error or issue are you seeing?
- What were you trying to do when it happened?

**Scope:**
- Which files or components are involved?
- When did this start happening?
- What changes were made recently?

**Confirmation:**
- I will investigate the [error] in [location], identify the root cause, and provide validated fix recommendations. Should I proceed?

### Architecture and Refactoring

**Intent:**
- What architecture changes are you trying to make?
- Why is this change needed?

**Scope:**
- Which components need to be refactored?
- Are there specific patterns or approaches you prefer?
- Any constraints on the new architecture?

**Confirmation:**
- I will refactor [components] from [current] to [target] architecture, following [approach]. Should I proceed?

### Documentation

**Intent:**
- What type of documentation do you need?
- Who is the target audience?

**Scope:**
- What topics should be covered?
- Any specific format requirements?
- Where should the documentation be saved?

**Confirmation:**
- I will create [type] documentation covering [topics] for [audience] and save to [location]. Should I proceed?

## Tips for Effective Questioning

**Do:**
- Ask open-ended questions to understand intent
- Offer options when there are clear choices
- Explain the implications of different options
- Confirm understanding before acting
- Batch related questions together

**Don't:**
- Assume you know what the user wants
- Skip questions to save time
- Present options without explanations
- Proceed without confirmation
- Ask too many questions at once (more than 4)
