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
