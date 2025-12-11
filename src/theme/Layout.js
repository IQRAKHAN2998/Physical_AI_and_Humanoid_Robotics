import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import Chatbot from '../components/chatbot/chatkit';
import { useLocation } from '@docusaurus/router';

// Create a wrapper component that adds the chatbot to all pages
export default function LayoutWrapper(props) {
  const { pathname } = useLocation();

  // Conditionally render the chatbot based on pathname if needed
  // For now, we'll show it on all pages
  const shouldShowChatbot = true;

  return (
    <>
      <OriginalLayout {...props} />
      {shouldShowChatbot && <Chatbot />}
    </>
  );
}