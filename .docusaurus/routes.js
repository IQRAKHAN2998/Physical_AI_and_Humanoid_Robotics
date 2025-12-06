import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/my_project',
    component: ComponentCreator('/my_project', 'bdf'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'f38'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '36f'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', 'b36'),
            routes: [
              {
                path: '/docs/assessments',
                component: ComponentCreator('/docs/assessments', '9ce'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/hardware-requirements',
                component: ComponentCreator('/docs/hardware-requirements', '663'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', '61d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/learning-outcomes',
                component: ComponentCreator('/docs/learning-outcomes', '769'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-1-ros2/nodes-topics-services',
                component: ComponentCreator('/docs/module-1-ros2/nodes-topics-services', '80b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-1-ros2/overview',
                component: ComponentCreator('/docs/module-1-ros2/overview', '27d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-1-ros2/rclpy-bridge',
                component: ComponentCreator('/docs/module-1-ros2/rclpy-bridge', 'af5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-1-ros2/urdf-humanoids',
                component: ComponentCreator('/docs/module-1-ros2/urdf-humanoids', '54c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-2-digital-twin/overview',
                component: ComponentCreator('/docs/module-2-digital-twin/overview', '692'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-2-digital-twin/physics-simulation',
                component: ComponentCreator('/docs/module-2-digital-twin/physics-simulation', '6b0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-2-digital-twin/simulating-sensors',
                component: ComponentCreator('/docs/module-2-digital-twin/simulating-sensors', '84e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-2-digital-twin/unity-interaction',
                component: ComponentCreator('/docs/module-2-digital-twin/unity-interaction', '8f7'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3-ai-robot-brain/isaac-ros',
                component: ComponentCreator('/docs/module-3-ai-robot-brain/isaac-ros', '8b2'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3-ai-robot-brain/isaac-sim',
                component: ComponentCreator('/docs/module-3-ai-robot-brain/isaac-sim', 'e1f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3-ai-robot-brain/nav2',
                component: ComponentCreator('/docs/module-3-ai-robot-brain/nav2', '68f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3-ai-robot-brain/overview',
                component: ComponentCreator('/docs/module-3-ai-robot-brain/overview', '043'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4-vla/capstone-project',
                component: ComponentCreator('/docs/module-4-vla/capstone-project', '8ce'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4-vla/cognitive-planning',
                component: ComponentCreator('/docs/module-4-vla/cognitive-planning', 'e6c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4-vla/overview',
                component: ComponentCreator('/docs/module-4-vla/overview', '0be'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4-vla/voice-to-action',
                component: ComponentCreator('/docs/module-4-vla/voice-to-action', 'eea'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/weekly-breakdown',
                component: ComponentCreator('/docs/weekly-breakdown', '776'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/why-physical-ai-matters',
                component: ComponentCreator('/docs/why-physical-ai-matters', '2f4'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '2e1'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
