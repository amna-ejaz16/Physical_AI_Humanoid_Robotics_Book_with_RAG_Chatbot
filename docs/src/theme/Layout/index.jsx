// src/theme/Layout/index.jsx
import React from 'react';
import Layout from '@theme-original/Layout';
import FloatingChatbot from '../../components/FloatingChatbot';

export default function LayoutWrapper(props) {
  return (
    <Layout {...props}>
      {props.children} {/* All site content */}

      {/* Floating chatbot mounted globally */}
      <FloatingChatbot />
    </Layout>
  );
}
