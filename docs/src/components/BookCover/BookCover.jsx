import React from 'react';
import { motion } from 'framer-motion';
import Link from '@docusaurus/Link';
import styles from './BookCover.module.css';

const modules = [
  {
    id: 1,
    title: 'Module 1',
    subtitle: 'ROS 2',
    description: 'Robot Operating System fundamentals',
    link: '/modules/module1-ros2/chapter1',
    icon: '🤖',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  },
  {
    id: 2,
    title: 'Module 2',
    subtitle: 'Digital Twin',
    description: 'Virtual robot simulation and modeling',
    link: '/modules/module2-digital-twin/chapter4',
    icon: '🔮',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  },
  {
    id: 3,
    title: 'Module 3',
    subtitle: 'AI Robot Brain',
    description: 'NVIDIA Isaac and intelligent control',
    link: '/modules/module3-isaac/chapter7',
    icon: '🧠',
    gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  },
  {
    id: 4,
    title: 'Module 4',
    subtitle: 'VLA Capstone',
    description: 'Vision-Language-Action integration',
    link: '/modules/module4-vla/chapter12',
    icon: '🎯',
    gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  },
];

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15,
      delayChildren: 0.3,
    },
  },
};

const item = {
  hidden: { opacity: 0, y: 30 },
  show: {
    opacity: 1,
    y: 0,
    transition: {
      type: 'spring',
      stiffness: 100,
      damping: 15,
    },
  },
};

const BookCover = () => {
  return (
    <div className={styles.bookCover}>
      {/* Hero Section */}
      <motion.div
        className={styles.hero}
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: 'easeOut' }}
      >
        <motion.h1
          className={styles.title}
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2, duration: 0.6 }}
        >
          Physical AI & Humanoid Robotics
        </motion.h1>

        <motion.p
          className={styles.tagline}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.6 }}
        >
          An AI-Powered Interactive Textbook
        </motion.p>

        <motion.p
          className={styles.subtitle}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.6 }}
        >
          Bridging Digital Brains and Physical Robots
        </motion.p>

        {/* Animated background elements */}
        <div className={styles.bgAnimation}>
          <motion.div
            className={styles.circle}
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.3, 0.5, 0.3],
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
          />
          <motion.div
            className={styles.circle}
            animate={{
              scale: [1.2, 1, 1.2],
              opacity: [0.2, 0.4, 0.2],
            }}
            transition={{
              duration: 5,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
          />
        </div>
      </motion.div>

      {/* Module Cards Section */}
      <motion.div
        id="modules"
        className={styles.modulesSection}
        variants={container}
        initial="hidden"
        animate="show"
      >
        <motion.h2
          className={styles.modulesTitle}
          variants={item}
        >
          Explore the Modules
        </motion.h2>

        <div className={styles.cardsGrid}>
          {modules.map((module) => (
            <motion.div
              key={module.id}
              variants={item}
              whileHover={{
                scale: 1.05,
                y: -8,
                transition: {
                  type: 'spring',
                  stiffness: 400,
                  damping: 25,
                },
              }}
              whileTap={{ scale: 0.98 }}
            >
              <Link to={module.link} className={styles.cardLink}>
                <div
                  className={styles.card}
                  style={{ background: module.gradient }}
                >
                  <div className={styles.cardIcon}>{module.icon}</div>
                  <h3 className={styles.cardTitle}>{module.title}</h3>
                  <h4 className={styles.cardSubtitle}>{module.subtitle}</h4>
                  <p className={styles.cardDescription}>{module.description}</p>
                  <div className={styles.cardArrow}>→</div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Call to Action */}
      <motion.div
        className={styles.cta}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5, duration: 0.8 }}
      >
        <p>Start your journey into the future of robotics</p>
      </motion.div>
    </div>
  );
};

export default BookCover;
