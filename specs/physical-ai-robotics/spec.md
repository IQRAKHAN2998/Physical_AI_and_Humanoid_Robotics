# Specification: Physical AI & Humanoid Robotics Textbook

## 1. Project Overview
- **Title:** Physical AI & Humanoid Robotics
- **Goal:** Create an AI-native textbook to teach a course in Physical AI & Humanoid Robotics, bridging the gap between digital AI and the physical body.
- **Target Audience:** Advanced AI students who want to build real humanoid robots.
- **Platform:** Docusaurus (classic template), using Markdown and MDX.
- **Content:** Technical, accurate, teachable, includes code blocks (ROS 2, Python, URDF), diagrams, and adheres to hardware tables, weekly breakdown, and learning outcomes from `Hackathon.md`.
- **Tone:** Professional but exciting.

## 2. Docusaurus Sidebar Structure (`sidebarCategories.js`)

```javascript
module.exports = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Course Introduction',
      link: {
        type: 'doc',
        id: 'intro/index',
      },
      items: [
        'intro/physical-ai-overview',
        'intro/learning-outcomes',
        'intro/assessments',
        'intro/hardware-requirements',
        'intro/cloud-native-option',
        'intro/economy-jetson-kit',
        'intro/latency-trap',
      ],
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      link: {
        type: 'doc',
        id: 'module1/index',
      },
      items: [
        'module1/week1-2-intro-physical-ai',
        'module1/week3-5-ros2-fundamentals',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      link: {
        type: 'doc',
        id: 'module2/index',
      },
      items: [
        'module2/week6-7-robot-simulation',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      link: {
        type: 'doc',
        id: 'module3/index',
      },
      items: [
        'module3/week8-10-nvidia-isaac-platform',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      link: {
        type: 'doc',
        id: 'module4/index',
      },
      items: [
        'module4/week11-12-humanoid-robot-development',
        'module4/week13-conversational-robotics',
        'module4/capstone-project',
      ],
    },
  ],
};
```

## 3. Chapter Details and Content Mapping

Each entry below describes a Docusaurus Markdown file:

### 3.1. Course Introduction Section (`docs/intro/`)

#### `docs/intro/index.md`
```markdown
---
id: intro/index
title: Course Introduction: Physical AI & Humanoid Robotics
sidebar_label: Introduction
sidebar_position: 1
---
```
**Content Mapping:**
- "## The Course Details" (Focus and Theme, Goal) from `Hackathon.md`
- "### Quarter Overview" from `Hackathon.md`
- "### Why Physical AI Matters" from `Hackathon.md`
- **Notes:** Serve as a general overview for the entire course.

#### `docs/intro/physical-ai-overview.md`
```markdown
---
id: intro/physical-ai-overview
title: Physical AI and Embodied Intelligence
sidebar_label: Physical AI Overview
sidebar_position: 2
---
```
**Content Mapping:**
- Detailed elaboration on "Foundations of Physical AI and embodied intelligence" from Weeks 1-2.
- Explanation of "From digital AI to robots that understand physical laws" from Weeks 1-2.
- Overview of "humanoid robotics landscape" from Weeks 1-2.
- Discussion of "Sensor systems: LIDAR, cameras, IMUs, force/torque sensors" from Weeks 1-2.
- **Code Examples:** Possibly simple Python examples for sensor data interpretation.
- **Diagrams:** Conceptual diagrams of embodied intelligence, sensor systems.

#### `docs/intro/learning-outcomes.md`
```markdown
---
id: intro/learning-outcomes
title: Learning Outcomes
sidebar_label: Learning Outcomes
sidebar_position: 3
---
```
**Content Mapping:**
- "### Learning Outcomes" (1-6) from `Hackathon.md` (exact reproduction).

#### `docs/intro/assessments.md`
```markdown
---
id: intro/assessments
title: Course Assessments
sidebar_label: Assessments
sidebar_position: 4
---
```
**Content Mapping:**
- "### Assessments" from `Hackathon.md` (exact reproduction).

#### `docs/intro/hardware-requirements.md`
```markdown
---
id: intro/hardware-requirements
title: Hardware Requirements
sidebar_label: Hardware Requirements
sidebar_position: 5
---
```
**Content Mapping:**
- "### Hardware Requirements"
    - "1. The "Digital Twin" Workstation (Required per Student)" from `Hackathon.md`
    - "2. The "Physical AI" Edge Kit" from `Hackathon.md`
    - "3. The Robot Lab" (Option A, B, C) from `Hackathon.md`
    - "4. Summary of Architecture" table from `Hackathon.md`
- **Diagrams:** Visual representations of workstation and edge kit setups.
- **Warning Boxes:** Emphasize GPU requirements (RTX), OS (Ubuntu), and RAM.

#### `docs/intro/cloud-native-option.md`
```markdown
---
id: intro/cloud-native-option
title: Cloud-Native ("Ether" Lab) Option
sidebar_label: Cloud-Native Lab
sidebar_position: 6
---
```
**Content Mapping:**
- "#### Option 2 High OpEx: The "Ether" Lab (Cloud-Native)" from `Hackathon.md`
- **Warning Boxes:** Highlight cost calculation and implications of cloud usage.

#### `docs/intro/economy-jetson-kit.md`
```markdown
---
id: intro/economy-jetson-kit
title: The Economy Jetson Student Kit
sidebar_label: Economy Jetson Kit
sidebar_position: 7
---
```
**Content Mapping:**
- "#### The Economy Jetson Student Kit" table from `Hackathon.md` (exact reproduction).

#### `docs/intro/latency-trap.md`
```markdown
---
id: intro/latency-trap
title: The Latency Trap (Hidden Cost)
sidebar_label: Latency Trap
sidebar_position: 8
---
```
**Content Mapping:**
- "#### 3. The Latency Trap (Hidden Cost)" from `Hackathon.md` (exact reproduction).
- **Warning Boxes:** Emphasize dangers of real-time robot control from cloud.

### 3.2. Module 1: The Robotic Nervous System (ROS 2) (`docs/module1/`)

#### `docs/module1/index.md`
```markdown
---
id: module1/index
title: Module 1: The Robotic Nervous System (ROS 2)
sidebar_label: Module 1 Overview
sidebar_position: 1
---
```
**Content Mapping:**
- "Module 1: The Robotic Nervous System (ROS 2)" description from `Hackathon.md` (Focus, ROS 2 Nodes, Topics, Services, rclpy, URDF).
- **Notes:** Introduction to the module.

#### `docs/module1/week1-2-intro-physical-ai.md`
```markdown
---
id: module1/week1-2-intro-physical-ai
title: Weeks 1-2: Introduction to Physical AI
sidebar_label: Weeks 1-2
sidebar_position: 2
---
```
**Content Mapping:**
- "Weeks 1-2: Introduction to Physical AI" from `Hackathon.md` (Foundations, Digital AI to robots, Humanoid robotics landscape, Sensor systems).
- **Notes:** This chapter will summarize briefly the topics covered in `intro/physical-ai-overview.md` and focus on the weekly context.

#### `docs/module1/week3-5-ros2-fundamentals.md`
```markdown
---
id: module1/week3-5-ros2-fundamentals
title: Weeks 3-5: ROS 2 Fundamentals
sidebar_label: Weeks 3-5
sidebar_position: 3
---
```
**Content Mapping:**
- "Weeks 3-5: ROS 2 Fundamentals" from `Hackathon.md` (ROS 2 architecture, Nodes, topics, services, actions, Python packages, Launch files, Parameter management).
- **Code Examples:** Extensive ROS 2 Python code for nodes, publishers, subscribers, services. URDF examples.
- **Diagrams:** ROS 2 communication graph, URDF structure.

### 3.3. Module 2: The Digital Twin (Gazebo & Unity) (`docs/module2/`)

#### `docs/module2/index.md`
```markdown
---
id: module2/index
title: Module 2: The Digital Twin (Gazebo & Unity)
sidebar_label: Module 2 Overview
sidebar_position: 1
---
```
**Content Mapping:**
- "Module 2: The Digital Twin (Gazebo & Unity)" description from `Hackathon.md` (Focus, Simulating physics, High-fidelity rendering, Simulating sensors).
- **Notes:** Introduction to the module.

#### `docs/module2/week6-7-robot-simulation.md`
```markdown
---
id: module2/week6-7-robot-simulation
title: Weeks 6-7: Robot Simulation with Gazebo
sidebar_label: Weeks 6-7
sidebar_position: 2
---
```
**Content Mapping:**
- "Weeks 6-7: Robot Simulation with Gazebo" from `Hackathon.md` (Gazebo setup, URDF/SDF, Physics/sensor simulation, Unity visualization).
- **Code Examples:** Gazebo world files, SDF/URDF models, ROS 2 integration with Gazebo.
- **Diagrams:** Gazebo simulation pipeline, Unity integration.

### 3.4. Module 3: The AI-Robot Brain (NVIDIA Isaac™) (`docs/module3/`)

#### `docs/module3/index.md`
```markdown
---
id: module3/index
title: Module 3: The AI-Robot Brain (NVIDIA Isaac™)
sidebar_label: Module 3 Overview
sidebar_position: 1
---
```
**Content Mapping:**
- "Module 3: The AI-Robot Brain (NVIDIA Isaac™)" description from `Hackathon.md` (Focus, Isaac Sim, Isaac ROS, Nav2).
- **Notes:** Introduction to the module.

#### `docs/module3/week8-10-nvidia-isaac-platform.md`
```markdown
---
id: module3/week8-10-nvidia-isaac-platform
title: Weeks 8-10: NVIDIA Isaac Platform
sidebar_label: Weeks 8-10
sidebar_position: 2
---
```
**Content Mapping:**
- "Weeks 8-10: NVIDIA Isaac Platform" from `Hackathon.md` (Isaac SDK/Sim, AI-powered perception/manipulation, Reinforcement learning, Sim-to-real).
- **Code Examples:** Isaac Sim Python scripts, Isaac ROS examples (VSLAM, navigation).
- **Diagrams:** Isaac Sim architecture, sim-to-real workflow.

### 3.5. Module 4: Vision-Language-Action (VLA) (`docs/module4/`)

#### `docs/module4/index.md`
```markdown
---
id: module4/index
title: Module 4: Vision-Language-Action (VLA)
sidebar_label: Module 4 Overview
sidebar_position: 1
---
```
**Content Mapping:**
- "Module 4: Vision-Language-Action (VLA)" description from `Hackathon.md` (Focus, Voice-to-Action, Cognitive Planning, Capstone Project).
- **Notes:** Introduction to the module.

#### `docs/module4/week11-12-humanoid-robot-development.md`
```markdown
---
id: module4/week11-12-humanoid-robot-development
title: Weeks 11-12: Humanoid Robot Development
sidebar_label: Weeks 11-12
sidebar_position: 2
---
```
**Content Mapping:**
- "Weeks 11-12: Humanoid Robot Development" from `Hackathon.md` (Kinematics/dynamics, Bipedal locomotion, Manipulation/grasping, Human-robot interaction).
- **Code Examples:** Kinematics libraries (e.g., KDL), bipedal walking algorithms.
- **Diagrams:** Humanoid kinematics, balance control.

#### `docs/module4/week13-conversational-robotics.md`
```markdown
---
id: module4/week13-conversational-robotics
title: Week 13: Conversational Robotics
sidebar_label: Week 13
sidebar_position: 3
---
```
**Content Mapping:**
- "Week 13: Conversational Robotics" from `Hackathon.md` (Integrating GPT models, Speech recognition, NLP, Multi-modal interaction).
- **Code Examples:** OpenAI Whisper API usage, LLM integration for task planning.
- **Diagrams:** Conversational AI pipeline for robots.

#### `docs/module4/capstone-project.md`
```markdown
---
id: module4/capstone-project
title: Capstone Project: The Autonomous Humanoid
sidebar_label: Capstone Project
sidebar_position: 4
---
```
**Content Mapping:**
- "Capstone Project: The Autonomous Humanoid" from `Hackathon.md` (simulated robot receives voice command, plans, navigates, identifies, manipulates).
- **Notes:** This chapter will outline the project, potentially link to example code repositories or provide a high-level architectural overview.

## 4. Docusaurus Configuration (`docusaurus.config.js`)
- Ensure the `docs` plugin is configured to use the `sidebarCategories.js` file for sidebar generation.

## 5. Directory Structure
```
docs/
├── intro/
│   ├── _category_.json
│   ├── index.md
│   ├── physical-ai-overview.md
│   ├── learning-outcomes.md
│   ├── assessments.md
│   ├── hardware-requirements.md
│   ├── cloud-native-option.md
│   ├── economy-jetson-kit.md
│   └── latency-trap.md
├── module1/
│   ├── _category_.json
│   ├── index.md
│   ├── week1-2-intro-physical-ai.md
│   └── week3-5-ros2-fundamentals.md
├── module2/
│   ├── _category_.json
│   ├── index.md
│   └── week6-7-robot-simulation.md
├── module3/
│   ├── _category_.json
│   ├── index.md
│   └── week8-10-nvidia-isaac-platform.md
├── module4/
│   ├── _category_.json
│   ├── index.md
│   ├── week11-12-humanoid-robot-development.md
│   ├── week13-conversational-robotics.md
│   └── capstone-project.md
└── sidebarCategories.js
```
