# Plan: Physical AI & Humanoid Robotics Textbook Generation

## 1. Scope and Dependencies

- **In Scope:**
    - Creation of all 25+ Markdown/MDX chapter files within the `docs/` directory, following the `specs/physical-ai-robotics/spec.md`.
    - Generation of `sidebarCategories.js`.
    - Inclusion of frontmatter for all chapters as specified.
    - Identification and placeholder generation for ROS 2 code examples, hardware comparison tables, and diagrams.
    - Detailed outline for the Capstone project chapter.
    - Content derived directly from `Hackathon.md` and the established Constitution.

- **Out of Scope:**
    - Actual Docusaurus setup or configuration beyond `sidebarCategories.js`.
    - Writing the complete narrative content for each chapter (only structure, frontmatter, and key elements like code/diagram placeholders).
    - Integration of RAG chatbot, signup/signin, personalization, or translation features (these are bonus points for the hackathon and not part of the core textbook generation plan).
    - Deployment of the Docusaurus site.

- **External Dependencies:**
    - `Hackathon.md`: Source of truth for course details, hardware, weekly breakdown, and learning outcomes.
    - `specs/physical-ai-robotics/spec.md`: Defines the exact file structure, chapter IDs, and content mapping.
    - Docusaurus: The target platform for the textbook.

## 2. Key Decisions and Rationale

- **Prioritization Strategy:** Following the user's explicit request: Introduction → Module 1 → Module 2 → Module 3 → Module 4 → Hardware → Weekly Breakdown → Assessments. This ensures foundational content is established first before diving into module-specific details.
- **Content Generation Approach:** For each chapter, the plan will outline: file path, Docusaurus frontmatter, primary content sections (mapped from `Hackathon.md`), and specific callouts for code examples, diagrams, or warning boxes.
- **Placeholder Usage:** Placeholder comments `<!-- CODE_EXAMPLE: [description] -->` or `<!-- DIAGRAM: [description] -->` will be used for future content to clearly indicate where technical assets are needed.
- **Docusaurus `_category_.json` files:** These will be created for each module to manage sidebar labels and positions effectively.

## 3. Interfaces and API Contracts (N/A for textbook generation)

## 4. Non-Functional Requirements (N/A for this planning phase)

## 5. Data Management and Migration (N/A for this planning phase)

## 6. Operational Readiness (N/A for this planning phase)

## 7. Risk Analysis and Mitigation

- **Risk:** Inconsistency between `Hackathon.md`, `specs/physical-ai-robotics/spec.md`, and generated chapter files.
    - **Mitigation:** Strict adherence to `spec.md` for all file paths, IDs, frontmatter, and content mapping. Double-checking generated output against the specification.
- **Risk:** Overlooking requirements for code examples, diagrams, or tables.
    - **Mitigation:** Explicitly listing these requirements for each chapter in the plan and using clear placeholders in the generated files.
- **Risk:** Incorrect Docusaurus sidebar structure.
    - **Mitigation:** Generating `sidebarCategories.js` based on `spec.md` and ensuring correct `_category_.json` files are created for each section.

## 8. Evaluation and Validation

- **Definition of Done:**
    - All Markdown/MDX files are created at their specified paths.
    - Each file contains correct Docusaurus frontmatter.
    - Each file includes content sections mapped from `Hackathon.md` (or detailed outlines for unique chapters like Capstone).
    - All required code example, diagram, and table placeholders are present.
    - `sidebarCategories.js` is correctly structured.
    - `_category_.json` files are present in module/intro directories.
- **Output Validation:** Manual review of generated files and `sidebarCategories.js` against `spec.md`.

## 9. Architectural Decision Record (ADR)

- No new significant architectural decisions beyond those captured in the specification for this planning phase. The decision on Docusaurus content architecture has already been suggested for an ADR.

## 10. Step-by-Step Execution Plan

### Phase 0: Setup
1.  Create `docs` directory if it doesn't exist.
2.  Create `docs/sidebarCategories.js` based on the structure in `specs/physical-ai-robotics/spec.md:27`.

### Phase 1: Course Introduction (`docs/intro/`)

1.  **Create `docs/intro/_category_.json`**
    - Content:
        ```json
        {
          "label": "Course Introduction",
          "position": 1,
          "link": {
            "type": "doc",
            "id": "intro/index"
          }
        }
        ```
2.  **Create `docs/intro/index.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:52`
    - Content Mapping: "## The Course Details" (Focus and Theme, Goal), "### Quarter Overview", "### Why Physical AI Matters" from `Hackathon.md`.
3.  **Create `docs/intro/physical-ai-overview.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:65`
    - Content Mapping: Elaboration on "Foundations of Physical AI and embodied intelligence", "From digital AI to robots that understand physical laws", "Overview of humanoid robotics landscape", "Sensor systems: LIDAR, cameras, IMUs, force/torque sensors" from `Hackathon.md` (Weeks 1-2 section).
    - **Needs:** Conceptual diagrams of embodied intelligence, sensor systems. Possibly simple Python code for sensor data interpretation.
4.  **Create `docs/intro/learning-outcomes.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:83`
    - Content Mapping: "### Learning Outcomes" (1-6) from `Hackathon.md`.
5.  **Create `docs/intro/assessments.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:92`
    - Content Mapping: "### Assessments" from `Hackathon.md`.
6.  **Create `docs/intro/hardware-requirements.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:101`
    - Content Mapping: "### Hardware Requirements" (Digital Twin Workstation, Physical AI Edge Kit, Robot Lab, Summary of Architecture table) from `Hackathon.md`.
    - **Needs:** Diagrams of workstation and edge kit setups. Warning boxes for GPU/OS/RAM.
7.  **Create `docs/intro/cloud-native-option.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:118`
    - Content Mapping: "#### Option 2 High OpEx: The "Ether" Lab (Cloud-Native)" from `Hackathon.md`.
    - **Needs:** Warning boxes for cost and latency implications.
8.  **Create `docs/intro/economy-jetson-kit.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:129`
    - Content Mapping: "#### The Economy Jetson Student Kit" table from `Hackathon.md`.
9.  **Create `docs/intro/latency-trap.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:139`
    - Content Mapping: "#### 3. The Latency Trap (Hidden Cost)" from `Hackathon.md`.
    - **Needs:** Warning boxes about dangers of real-time robot control from cloud.

### Phase 2: Module 1: The Robotic Nervous System (ROS 2) (`docs/module1/`)

1.  **Create `docs/module1/_category_.json`**
    - Content:
        ```json
        {
          "label": "Module 1: The Robotic Nervous System (ROS 2)",
          "position": 2,
          "link": {
            "type": "doc",
            "id": "module1/index"
          }
        }
        ```
2.  **Create `docs/module1/index.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:154`
    - Content Mapping: "Module 1: The Robotic Nervous System (ROS 2)" description (Focus, ROS 2 Nodes, Topics, Services, rclpy, URDF) from `Hackathon.md`.
3.  **Create `docs/module1/week1-2-intro-physical-ai.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:164`
    - Content Mapping: Summarize "Weeks 1-2: Introduction to Physical AI" from `Hackathon.md` focusing on weekly context.
4.  **Create `docs/module1/week3-5-ros2-fundamentals.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:175`
    - Content Mapping: "Weeks 3-5: ROS 2 Fundamentals" (ROS 2 architecture, Nodes, topics, services, actions, Python packages, Launch files, Parameter management) from `Hackathon.md`.
    - **Needs:** Extensive ROS 2 Python code examples for nodes, publishers, subscribers, services. URDF examples. Diagrams of ROS 2 communication graph, URDF structure.

### Phase 3: Module 2: The Digital Twin (Gazebo & Unity) (`docs/module2/`)

1.  **Create `docs/module2/_category_.json`**
    - Content:
        ```json
        {
          "label": "Module 2: The Digital Twin (Gazebo & Unity)",
          "position": 3,
          "link": {
            "type": "doc",
            "id": "module2/index"
          }
        }
        ```
2.  **Create `docs/module2/index.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:190`
    - Content Mapping: "Module 2: The Digital Twin (Gazebo & Unity)" description (Focus, Simulating physics, High-fidelity rendering, Simulating sensors) from `Hackathon.md`.
3.  **Create `docs/module2/week6-7-robot-simulation.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:200`
    - Content Mapping: "Weeks 6-7: Robot Simulation with Gazebo" (Gazebo setup, URDF/SDF, Physics/sensor simulation, Unity visualization) from `Hackathon.md`.
    - **Needs:** Code examples for Gazebo world files, SDF/URDF models, ROS 2 integration with Gazebo. Diagrams of Gazebo simulation pipeline, Unity integration.

### Phase 4: Module 3: The AI-Robot Brain (NVIDIA Isaac™) (`docs/module3/`)

1.  **Create `docs/module3/_category_.json`**
    - Content:
        ```json
        {
          "label": "Module 3: The AI-Robot Brain (NVIDIA Isaac™)",
          "position": 4,
          "link": {
            "type": "doc",
            "id": "module3/index"
          }
        }
        ```
2.  **Create `docs/module3/index.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:215`
    - Content Mapping: "Module 3: The AI-Robot Brain (NVIDIA Isaac™)" description (Focus, Isaac Sim, Isaac ROS, Nav2) from `Hackathon.md`.
3.  **Create `docs/module3/week8-10-nvidia-isaac-platform.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:225`
    - Content Mapping: "Weeks 8-10: NVIDIA Isaac Platform" (Isaac SDK/Sim, AI-powered perception/manipulation, Reinforcement learning, Sim-to-real) from `Hackathon.md`.
    - **Needs:** Code examples for Isaac Sim Python scripts, Isaac ROS examples (VSLAM, navigation). Diagrams of Isaac Sim architecture, sim-to-real workflow.

### Phase 5: Module 4: Vision-Language-Action (VLA) (`docs/module4/`)

1.  **Create `docs/module4/_category_.json`**
    - Content:
        ```json
        {
          "label": "Module 4: Vision-Language-Action (VLA)",
          "position": 5,
          "link": {
            "type": "doc",
            "id": "module4/index"
          }
        }
        ```
2.  **Create `docs/module4/index.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:240`
    - Content Mapping: "Module 4: Vision-Language-Action (VLA)" description (Focus, Voice-to-Action, Cognitive Planning, Capstone Project) from `Hackathon.md`.
3.  **Create `docs/module4/week11-12-humanoid-robot-development.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:250`
    - Content Mapping: "Weeks 11-12: Humanoid Robot Development" (Kinematics/dynamics, Bipedal locomotion, Manipulation/grasping, Human-robot interaction) from `Hackathon.md`.
    - **Needs:** Code examples for kinematics libraries (e.g., KDL), bipedal walking algorithms. Diagrams of humanoid kinematics, balance control.
4.  **Create `docs/module4/week13-conversational-robotics.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:261`
    - Content Mapping: "Week 13: Conversational Robotics" (Integrating GPT models, Speech recognition, NLP, Multi-modal interaction) from `Hackathon.md`.
    - **Needs:** Code examples for OpenAI Whisper API usage, LLM integration for task planning. Diagrams of conversational AI pipeline for robots.
5.  **Create `docs/module4/capstone-project.md`**
    - Frontmatter: `specs/physical-ai-robotics/spec.md:272`
    - Content Mapping: "Capstone Project: The Autonomous Humanoid" from `Hackathon.md` (simulated robot receives voice command, plans, navigates, identifies, manipulates).
    - **Needs:** Detailed outline of project structure, high-level architectural overview, potential links to example code repositories, breakdown of key challenges.

## 11. `docusaurus.config.js` and `_category_.json` Files

- Ensure `docusaurus.config.js` properly points to `sidebarCategories.js`.
- All `_category_.json` files will be created in their respective directories (`docs/intro`, `docs/module1`, etc.) as outlined in the plan.
