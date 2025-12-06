# Project Constitution: Physical AI & Humanoid Robotics Textbook

## 1. Core Mission & Vision
- **Vision:** To create the definitive AI-native textbook for teaching Physical AI & Humanoid Robotics, empowering advanced AI students to build and control real humanoid robots.
- **Mission:** To bridge the gap between digital AI and the physical world through a comprehensive Docusaurus-based textbook, incorporating cutting-edge research, practical code examples (ROS 2, Python, URDF), and real-world hardware considerations.

## 2. Development Guidelines

### 2.1. Content Principles
- **Accuracy & Depth:** All chapters must be technically accurate, current, and provide in-depth understanding.
- **Teachability:** Content must be structured for effective learning, with clear explanations and logical progression.
- **Practicality:** Emphasize practical application, including relevant code blocks (ROS 2, Python, URDF, etc.) and hardware considerations.
- **Hackathon Alignment:** Strictly adhere to the hackathon brief, including course syllabus, hardware tables, weekly breakdowns, and learning outcomes as documented in `Hackathon.md`.
- **Docusaurus & MDX:** The book will be written exclusively using Markdown and MDX, within the `docs/` folder, leveraging Docusaurus features for structure and presentation.
- **Sidebar Structure:** Implement a proper sidebar structure with modules and weeks, mirroring the course outline.

### 2.2. Tone & Style
- **Professional but Exciting:** Maintain a professional academic tone while conveying the excitement and transformative potential of humanoid robotics.
- **Target Audience:** Written for advanced AI students with a strong technical background, aspiring to build real humanoid robots.
- **Conciseness:** Chapters should be comprehensive but avoid unnecessary jargon or verbosity.

### 2.3. Technical Standards
- **Code Quality:** Code examples must be clean, well-commented (where necessary for clarity), and follow best practices for ROS 2 and Python development.
- **Reproducibility:** Code examples should be reproducible in simulated (Gazebo, NVIDIA Isaac Sim) and, where applicable, physical environments.
- **Version Control:** All content and code will be managed under Git version control.

## 3. Architecture Principles (for the textbook itself)
- **Modularity:** Content organized into distinct modules and weeks for clear navigation and learning progression.
- **Interactivity (Future-Proof):** Designed to integrate future AI-native features like RAG chatbots and personalized content (as per hackathon bonus points).
- **Scalability:** Structure allows for easy addition of new chapters, modules, or updates.

## 4. Non-Functional Requirements (for the textbook itself)
- **Performance (Website):** Fast loading times for Docusaurus site.
- **Accessibility:** Adhere to web accessibility standards for documentation.
- **Maintainability:** Easy to update and extend content.

## 5. Security Principles (for the textbook and any integrated features)
- **No Hardcoded Secrets:** Any configuration or integration with external services (e.g., OpenAI API keys for RAG chatbot) must use environment variables or secure configuration management.
- **Input Validation:** For any interactive components (like future RAG chatbot), rigorous input validation to prevent injection attacks (e.g., XSS).
- **Least Privilege:** Any integrated services or scripts will operate with the minimum necessary permissions.

## 6. Project Artifacts & Standards
- **Prompt History Records (PHRs):** Every significant interaction and decision will be documented in PHRs under `history/prompts/`.
- **Architectural Decision Records (ADRs):** Significant architectural decisions related to the book's structure or integrated features will be documented as ADRs under `history/adr/`, when prompted by the user.
- **Spec-Kit Plus Compliance:** Adhere to Spec-Kit Plus directory structure and principles for specifications, plans, and tasks.

## 7. Hardware & Software Ecosystem (as per Hackathon.md)

### 7.1. Software Stack
- ROS 2 (Humble/Iron)
- Gazebo & Unity
- NVIDIA Isaac SDK, Isaac Sim, Isaac ROS, Nav2
- OpenAI Agents/ChatKit SDKs
- FastAPI
- Neon Serverless Postgres
- Qdrant Cloud Free Tier
- Docusaurus (for book platform)

### 7.2. Hardware Requirements (Digital Twin Workstation - Required per Student)
- **GPU:** NVIDIA RTX 4070 Ti (12GB VRAM) or higher (Ideal: RTX 3090/4090 with 24GB VRAM)
- **CPU:** Intel Core i7 (13th Gen+) or AMD Ryzen 9
- **RAM:** 64 GB DDR5 (32 GB minimum)
- **OS:** Ubuntu 22.04 LTS (mandatory for ROS 2 compatibility)

### 7.3. Hardware Requirements (Physical AI Edge Kit)
- **Brain:** NVIDIA Jetson Orin Nano (8GB) or Orin NX (16GB)
- **Eyes (Vision):** Intel RealSense D435i or D455 (includes IMU)
- **Inner Ear (Balance):** Generic USB IMU (BNO055) (often built-in, or separate module for calibration learning)
- **Voice Interface:** Simple USB Microphone/Speaker array (e.g., ReSpeaker)

### 7.4. Robot Lab Options
- **Option A (Proxy):** Unitree Go2 Edu (quadruped or robotic arm)
- **Option B (Miniature Humanoid):** Unitree G1 (~$16k) or Robotis OP3 (~$12k); Budget Alternative: Hiwonder TonyPi Pro (~$600, note Raspberry Pi limitations for NVIDIA Isaac ROS)
- **Option C (Premium Sim-to-Real):** Unitree G1 Humanoid

### 7.5. Summary of Architecture (Hardware)
| Component | Hardware | Function |
|---|---|---|
| Sim Rig | PC with RTX 4080 + Ubuntu 22.04 | Runs Isaac Sim, Gazebo, Unity, and trains LLM/VLA models |
| Edge Brain | Jetson Orin Nano | Runs the "Inference" stack. Students deploy their code here |
| Sensors | RealSense Camera + Lidar | Connected to the Jetson to feed real-world data to the AI |
| Actuator | Unitree Go2 or G1 (Shared) | Receives motor commands from the Jetson |

### 7.6. Cloud-Native ("Ether" Lab) Option
- **Cloud Workstations:** AWS g5.2xlarge (A10G GPU, 24GB VRAM) or g6e.xlarge with NVIDIA Isaac Sim on Omniverse Cloud.
- **Local "Bridge" Hardware:** Jetson Kit for physical deployment.
- **Latency Trap:** Cloud training, local flashing of models to Jetson kit to avoid latency issues with real robot control.

## 8. Learning Outcomes (from Hackathon.md)
1. Understand Physical AI principles and embodied intelligence
2. Master ROS 2 (Robot Operating System) for robotic control
3. Simulate robots with Gazebo and Unity
4. Develop with NVIDIA Isaac AI robot platform
5. Design humanoid robots for natural interactions
6. Integrate GPT models for conversational robotics

## 9. Weekly Breakdown (from Hackathon.md)
- **Weeks 1-2:** Introduction to Physical AI
- **Weeks 3-5:** ROS 2 Fundamentals
- **Weeks 6-7:** Robot Simulation with Gazebo
- **Weeks 8-10:** NVIDIA Isaac Platform
- **Weeks 11-12:** Humanoid Robot Development
- **Week 13:** Conversational Robotics

## 10. Assessments (from Hackathon.md)
- ROS 2 package development project
- Gazebo simulation implementation
- Isaac-based perception pipeline
- Capstone: Simulated humanoid robot with conversational AI
