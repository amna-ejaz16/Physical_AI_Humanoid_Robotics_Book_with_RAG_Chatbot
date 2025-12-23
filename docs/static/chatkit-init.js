/**
 * ChatKit Widget Initialization
 * This script creates and configures the ChatKit floating widget
 * for the Docusaurus Physical AI & Humanoid Robotics book.
 */

// Configuration
const CHATKIT_CONFIG = {
  // Backend API endpoint (change for production)
  backendUrl: window.CHATKIT_BACKEND_URL || 'http://localhost:8000/ask',

  // Domain key for verification
  domainKey: 'docusaurus-physical-ai-book',

  // Theme configuration
  theme: {
    colorScheme: 'light',
    radius: 'round',
    color: {
      accent: {
        primary: '#3B82F6', // Blue accent color
        level: 2
      }
    }
  },

  // Start screen configuration
  startPrompts: [
    {
      label: 'What is Physical AI?',
      prompt: 'Can you explain what physical AI means and how it differs from traditional AI?',
      icon: 'robot'
    },
    {
      label: 'Humanoid Components',
      prompt: 'What are the main components and subsystems of a humanoid robot?',
      icon: 'settings'
    },
    {
      label: 'Control Systems',
      prompt: 'How do humanoid robot control systems work for bipedal locomotion?',
      icon: 'brain'
    },
    {
      label: 'Sensor Integration',
      prompt: 'How do humanoid robots integrate data from multiple sensors?',
      icon: 'eye'
    }
  ]
};

// Initialize ChatKit when DOM is ready
function initializeChatKit() {
  // Import ChatKit library
  import('https://cdn.platform.openai.com/deployments/chatkit/chatkit.js')
    .then(() => {
      console.log('[ChatKit] Library loaded successfully');

      // Create ChatKit element
      const chatkit = document.createElement('openai-chatkit');

      // Configure ChatKit options
      chatkit.setOptions({
        api: {
          url: CHATKIT_CONFIG.backendUrl,
          domainKey: CHATKIT_CONFIG.domainKey,

          // Custom fetch to transform request/response if needed
          fetch: async (url, options) => {
            try {
              // Add custom headers if needed
              const customOptions = {
                ...options,
                headers: {
                  ...options.headers,
                  'Content-Type': 'application/json'
                }
              };

              // Make request to backend
              const response = await fetch(url, customOptions);

              // Handle errors
              if (!response.ok) {
                const errorData = await response.json();
                console.error('[ChatKit] Backend error:', errorData);

                // Return error response in expected format
                return new Response(
                  JSON.stringify({
                    error: errorData.error || 'Failed to get response',
                    metadata: {
                      error_code: errorData.error_code,
                      request_id: errorData.request_id
                    }
                  }),
                  {
                    status: response.status,
                    headers: response.headers
                  }
                );
              }

              return response;
            } catch (error) {
              console.error('[ChatKit] Network error:', error);

              // Return network error response
              return new Response(
                JSON.stringify({
                  error: 'Unable to connect to the server. Please try again.',
                  metadata: { error_code: 'NETWORK_ERROR' }
                }),
                { status: 500 }
              );
            }
          }
        },

        theme: CHATKIT_CONFIG.theme,

        header: {
          enabled: true,
          title: {
            text: 'Book Assistant'
          }
        },

        history: {
          enabled: true,
          showDelete: true,
          showRename: true
        },

        startScreen: {
          greeting: 'Ask me anything about Physical AI & Humanoid Robotics!',
          prompts: CHATKIT_CONFIG.startPrompts
        },

        composer: {
          placeholder: 'Ask about the book content...'
        },

        threadItemActions: {
          feedback: true, // Allow user feedback
          retry: true // Allow retry on errors
        }
      });

      // Add ChatKit to page
      document.body.appendChild(chatkit);

      console.log('[ChatKit] Widget initialized successfully');
    })
    .catch(error => {
      console.error('[ChatKit] Failed to load:', error);
    });
}

// Wait for DOM to be ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeChatKit);
} else {
  initializeChatKit();
}
