---
sidebar_position: 2
title: Nodes, Topics, and Services
---

### ROS 2 Nodes, Topics, and Services

In ROS 2, the core building blocks for robot software are nodes, topics, and services. A **node** is a single executable that performs computation, such as reading sensor data, controlling actuators, or running AI algorithms. By dividing a robot’s functionality into multiple nodes, ROS 2 enables modular, scalable, and maintainable software architectures.

**Topics** provide a publish-subscribe communication mechanism between nodes. For example, a camera node can publish images to a `/camera` topic, and a processing node can subscribe to this topic to perform image analysis in real-time. This asynchronous communication allows multiple nodes to share data efficiently without tight coupling.

**Services** enable synchronous, request-response interactions between nodes. Unlike topics, services are used when a node needs an immediate response from another node. For instance, a motion planning node might request the current robot pose from a localization node using a service call, and wait for the result before proceeding.

Together, nodes, topics, and services form the backbone of ROS 2 middleware. Students will gain hands-on experience by creating Python nodes using `rclpy`, publishing and subscribing to topics, and implementing simple service calls. By the end of this module, learners will understand how these concepts enable reliable communication and coordination between multiple components of a humanoid robot, forming the foundation for AI-driven robotic behaviors.
