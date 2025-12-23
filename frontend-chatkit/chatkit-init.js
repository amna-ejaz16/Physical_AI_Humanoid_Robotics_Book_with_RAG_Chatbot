/**
 * Chat Widget Initialization
 * Floating chat iframe for Docusaurus book
 */

// Initialize Chat when DOM is ready
function initializeChatKit() {
  console.log('[ChatKit] Initializing widget');

  // Prevent duplicate widget
  if (document.getElementById('chatkit-container')) return;

  const container = document.createElement('div');
  container.id = 'chatkit-container';
  container.style.position = 'fixed';
  container.style.bottom = '20px';
  container.style.right = '20px';
  container.style.zIndex = '9999';

  container.innerHTML = `
    <iframe
      src="http://localhost:8000/chat"
      style="
        width:360px;
        height:600px;
        border:none;
        border-radius:12px;
        box-shadow:0 4px 16px rgba(0,0,0,.2);
      "
      allow="clipboard-write"
    ></iframe>
  `;

  document.body.appendChild(container);
  console.log('[ChatKit] Widget mounted successfully');
}

// Run on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeChatKit);
} else {
  initializeChatKit();
}
