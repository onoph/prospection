chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Message received:', message);
  if (message.action === "close_tab" && sender.tab?.id) {
    console.log('Closing tab:', sender.tab.id);
    chrome.tabs.remove(sender.tab.id);
  }
});