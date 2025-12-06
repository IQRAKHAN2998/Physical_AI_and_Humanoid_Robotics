const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1-ros2/overview',
        'module-1-ros2/nodes-topics-services',
        'module-1-ros2/rclpy-bridge',
        'module-1-ros2/urdf-humanoids',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module-2-digital-twin/overview',
        'module-2-digital-twin/physics-simulation',
        'module-2-digital-twin/unity-interaction',
        'module-2-digital-twin/simulating-sensors',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'module-3-ai-robot-brain/overview',
        'module-3-ai-robot-brain/isaac-sim',
        'module-3-ai-robot-brain/isaac-ros',
        'module-3-ai-robot-brain/nav2',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module-4-vla/overview',
        'module-4-vla/voice-to-action',
        'module-4-vla/cognitive-planning',
        'module-4-vla/capstone-project',
      ],
    },
    'why-physical-ai-matters',
    'learning-outcomes',
    'weekly-breakdown',
    'assessments',
    'hardware-requirements',
  ],
};

module.exports = sidebars;

// /**
//  * Creating a sidebar enables you to:
//  * - Create an ordered group of docs
//  * - Render a sidebar in the docs side navigation
//  * - Learn more about Docusaurus sidebars: https://docusaurus.io/docs/sidebar
//  */

// // @ts-check

// /** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
// const sidebars = {
//   tutorialSidebar: [
//     'intro',
//     {
//       type: 'category',
//       label: 'Module 1: The Robotic Nervous System (ROS 2)',
//       items: [
//         'module-1-ros2/01-overview',
//         'module-1-ros2/02-nodes-topics-services',
//         'module-1-ros2/03-rclpy-bridge',
//         'module-1-ros2/04-urdf-humanoids',
//       ],
//     },
//     {
//       type: 'category',
//       label: 'Module 2: The Digital Twin (Gazebo & Unity)',
//       items: [
//         'module-2-digital-twin/01-overview',
//         'module-2-digital-twin/02-physics-simulation',
//         'module-2-digital-twin/03-unity-interaction',
//         'module-2-digital-twin/04-simulating-sensors',
//       ],
//     },
//     {
//       type: 'category',
//       label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
//       items: [
//         'module-3-ai-robot-brain/01-overview',
//         'module-3-ai-robot-brain/02-isaac-sim',
//         'module-3-ai-robot-brain/03-isaac-ros',
//         'module-3-ai-robot-brain/04-nav2',
//       ],
//     },
//     {
//       type: 'category',
//       label: 'Module 4: Vision-Language-Action (VLA)',
//       items: [
//         'module-4-vla/01-overview',
//         'module-4-vla/02-voice-to-action',
//         'module-4-vla/03-cognitive-planning',
//         'module-4-vla/04-capstone-project',
//       ],
//     },
//     'why-physical-ai-matters',
//     'learning-outcomes',
//     'weekly-breakdown',
//     'assessments',
//     'hardware-requirements',
//   ],
// };


// export default sidebars;
