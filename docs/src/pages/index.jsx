import React from 'react';
import Layout from '@theme/Layout';
import BookCover from '@site/src/components/BookCover/BookCover';

export default function Home() {
  return (
    <Layout
      title="Home"
      description="Physical AI & Humanoid Robotics - An AI-Powered Interactive Textbook"
    >
      <BookCover />
    </Layout>
  );
}
