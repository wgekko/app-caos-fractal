document.addEventListener('DOMContentLoaded', function() {
  // Terminal button effects
  const terminalButtons = document.querySelectorAll('.terminal-button');
  
  terminalButtons.forEach(button => {
    button.addEventListener('click', function() {
      if (button.classList.contains('close')) {
        alert('System Collapse Report cannot be dismissed during global network failure');
      } else if (button.classList.contains('minimize')) {
        document.querySelector('.content').classList.toggle('minimized');
      }
    });
  });

  // Real countdown timer
  const countdownElement = document.getElementById('countdown');
  let minutes = 1;
  let seconds = 30;
  
  function updateCountdown() {
    if (!countdownElement) return; // Safety check
    
    countdownElement.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    
    if (minutes === 0 && seconds === 0) {
      minutes = Math.floor(Math.random() * 3) + 2;
      seconds = Math.floor(Math.random() * 60);
      
      const reconnectStatus = document.querySelector('.reconnect-status');
      if (reconnectStatus) {
        reconnectStatus.textContent = `FAILED - RETRYING IN ${countdownElement.textContent}`;
        reconnectStatus.style.color = '#ff3333';
      }
      
      triggerCatastrophicGlitch(); // Make sure this function exists
    } else {
      if (seconds === 0) {
        minutes--;
        seconds = 59;
      } else {
        seconds--;
      }
    }
    
    setTimeout(updateCountdown, 1000);
  }
  
  updateCountdown();

  // Error codes and glitch text collection
  const errorTypes = [
    { code: "ERR_CONNECTION_RESET", detail: "0x8007274C" },
    { code: "SEGFAULT", detail: "core dumped: 0xB00B1E5" },
    { code: "CRITICAL_PROCESS_DIED", detail: "ntdll.dll" },
    { code: "CONNECTION_INTERRUPTED", detail: "timeout: 30000ms" },
    { code: "404_NOT_FOUND", detail: "/dns/root" },
    { code: "EXCEPTION_ACCESS_VIOLATION", detail: "0x00000000" },
    { code: "DNS_PROBE_FAILED", detail: "ERR_NAME_RESOLUTION" },
    { code: "KERNEL_PANIC", detail: "unable to mount root fs" },
    { code: "STACK_OVERFLOW", detail: "recursion limit reached" },
    { code: "FATAL_ERROR", detail: "memory allocation failed" },
    { code: "NETWORK_UNREACHABLE", detail: "127.0.0.1" },
    { code: "SYSTEM_HALT", detail: "0xDEAD_BEEF" }
  ];
  
  // Binary data for extreme glitches
  const binaryData = [
    "01001110 01000101 01010100 01010111 01001111 01010010",
    "01000011 01001111 01001100 01001100 01000001 01010000",
    "01000110 01000001 01001001 01001100 01000101 01000100",
    "01000100 01001110 01010011 01000101 01010010 01010010"
  ];

  // Function to create glitched text
  function createGlitchedText(original, severity = 'medium') {
    if (!original) return original;
    
    const errorSnippet = errorTypes[Math.floor(Math.random() * errorTypes.length)];
    
    // Different severity levels for different effects
    switch(severity) {
      case 'mild':
        // Just replace a random word with an error code
        const words = original.split(' ');
        if (words.length > 2) {
          const replaceIndex = Math.floor(Math.random() * words.length);
          words[replaceIndex] = `<span class="code-glitch">${errorSnippet.code}</span>`;
          return words.join(' ');
        } else {
          return `<span class="code-glitch">${errorSnippet.code}</span>`;
        }
        
      case 'medium':
        // Replace content with error code and detail
        return `<span class="code-glitch">${errorSnippet.code}</span> <span class="code-glitch-detail">${errorSnippet.detail}</span>`;
        
      case 'severe':
        // Full binary corruption
        const binary = binaryData[Math.floor(Math.random() * binaryData.length)];
        return `<span class="binary-glitch">${binary}</span>`;
        
      default:
        return original;
    }
  }

  // Random text glitch effect
  function randomTextGlitch() {
    const potentialTargets = [
      { selector: '.system-message', chance: 0.3, severity: 'medium' },
      { selector: 'p:not(.dev-note):not(.system-message)', chance: 0.15, severity: 'mild' },
      { selector: '.status', chance: 0.12, severity: 'medium' },
      { selector: '.event-header', chance: 0.08, severity: 'mild' },
      { selector: '.region-status-indicator', chance: 0.04, severity: 'mild' },
      { selector: '.terminal-title', chance: 0.03, severity: 'severe' },
      { selector: '.alert-text', chance: 0.02, severity: 'severe' }
    ];
    
    potentialTargets.forEach(target => {
      const elements = document.querySelectorAll(target.selector);
      
      elements.forEach(element => {
        if (Math.random() < target.chance) {
          // Store original content if not already stored
          if (!element.dataset.original) {
            element.dataset.original = element.innerHTML || element.textContent;
          }
          
          // Apply glitch
          element.innerHTML = createGlitchedText(element.dataset.original, target.severity);
          
          // Add visual distortion class
          element.classList.add('visual-glitch');
          
          // Restore after a random time
          setTimeout(() => {
            element.innerHTML = element.dataset.original;
            element.classList.remove('visual-glitch');
          }, Math.random() * 500 + 300);
        }
      });
    });
    
    // Schedule next glitch
    setTimeout(randomTextGlitch, Math.random() * 2500 + 1000);
  }

  // Start random text glitches
  randomTextGlitch();

  // Visual element glitches (subtle movement/distortion)
  function randomVisualGlitch() {
    const targets = [
      '.events li',
      '.services li',
      '.region',
      '.reconnect-attempt',
      '.world-map'
    ];
    
    const randomSelector = targets[Math.floor(Math.random() * targets.length)];
    const elements = document.querySelectorAll(randomSelector);
    
    if (elements.length > 0) {
      const element = elements[Math.floor(Math.random() * elements.length)];
      
      // Random visual glitch effect
      const glitchType = Math.floor(Math.random() * 5);
      
      switch(glitchType) {
        case 0: // Horizontal displacement
          element.style.transform = `translateX(${Math.random() * 4 - 2}px)`;
          setTimeout(() => {
            element.style.transform = '';
          }, Math.random() * 150 + 50);
          break;
          
        case 1: // Opacity flicker
          element.style.opacity = '0.7';
          setTimeout(() => {
            element.style.opacity = '';
          }, Math.random() * 100 + 50);
          break;
          
        case 2: // Color distortion
          element.style.filter = `hue-rotate(${Math.random() * 30}deg)`;
          setTimeout(() => {
            element.style.filter = '';
          }, Math.random() * 200 + 100);
          break;
          
        case 3: // Brief blur
          element.style.filter = `blur(${Math.random() * 2 + 1}px)`;
          setTimeout(() => {
            element.style.filter = '';
          }, Math.random() * 100 + 50);
          break;
          
        case 4: // Skew distortion
          element.style.transform = `skew(${Math.random() * 5 - 2.5}deg, ${Math.random() * 2 - 1}deg)`;
          setTimeout(() => {
            element.style.transform = '';
          }, Math.random() * 150 + 50);
          break;
      }
    }
    
    // Schedule next visual glitch
    setTimeout(randomVisualGlitch, Math.random() * 3000 + 1000);
  }
  
  // Start visual glitches
  randomVisualGlitch();

  // Occasional screen-wide glitch effects
  function screenGlitch() {
    if (Math.random() > 0.7) {
      const content = document.querySelector('.content');
      const glitchType = Math.floor(Math.random() * 5);
      
      switch(glitchType) {
        case 0: // Color channel shift
          content.style.transform = 'scale(1.003)';
          content.style.filter = 'contrast(1.2) hue-rotate(5deg)';
          content.classList.add('rgb-shift');
          break;
          
        case 1: // Vertical scanning line
          const scanLine = document.createElement('div');
          scanLine.className = 'scan-line';
          content.appendChild(scanLine);
          setTimeout(() => {
            scanLine.remove();
          }, 1000);
          break;
          
        case 2: // Brief flash
          content.style.filter = 'brightness(1.5) contrast(1.2)';
          break;
          
        case 3: // Noise effect
          content.classList.add('noise-effect');
          break;
          
        case 4: // Digital distortion
          content.classList.add('digital-distortion');
          break;
      }
      
      // Clear effects after short delay
      setTimeout(() => {
        content.style.transform = '';
        content.style.filter = '';
        content.classList.remove('rgb-shift', 'noise-effect', 'digital-distortion');
      }, Math.random() * 200 + 100);
    }
    
    // Schedule next screen glitch
    setTimeout(screenGlitch, Math.random() * 10000 + 5000);
  }
  
  // Start screen glitches
  screenGlitch();

  // Catastrophic effects when countdown reaches zero
  function triggerCatastrophicGlitch() {
    // Screen-wide effect
    const content = document.querySelector('.content');
    content.classList.add('catastrophic-failure');
    
    // Corrupt multiple text elements
    const textElements = document.querySelectorAll('.system-message, .status, h2, h3, .region-status-indicator');
    
    textElements.forEach(element => {
      if (Math.random() > 0.3) {
        if (!element.dataset.original) {
          element.dataset.original = element.innerHTML || element.textContent;
        }
        
        if (Math.random() > 0.5) {
          // Error code corruption
          element.innerHTML = createGlitchedText('', 'medium');
        } else {
          // Binary corruption
          element.innerHTML = createGlitchedText('', 'severe');
        }
        
        element.classList.add('critical-glitch');
      }
    });
    
    // Add scan line effects
    const scanLine = document.createElement('div');
    scanLine.className = 'heavy-scan';
    scanLine.style.position = 'absolute';
    scanLine.style.top = '0';
    scanLine.style.left = '0';
    scanLine.style.width = '100%';
    scanLine.style.height = '100%';
    scanLine.style.background = 'linear-gradient(transparent, rgba(255, 50, 50, 0.2), transparent)';
    scanLine.style.animation = 'scan-line 2s linear infinite';
    scanLine.style.pointerEvents = 'none';
    scanLine.style.zIndex = '1000';
    content.appendChild(scanLine);
    
    // Restore after a delay
    setTimeout(() => {
      content.classList.remove('catastrophic-failure');
      scanLine.remove();
      
      textElements.forEach(element => {
        if (element.dataset.original) {
          element.innerHTML = element.dataset.original;
          element.classList.remove('critical-glitch');
        }
      });
    }, 2000);
  }

  // Initialize regions with random states
  function initializeRegionsWithRandomStates() {
    const regions = document.querySelectorAll('.region');
    const continents = document.querySelectorAll('.continent');
    
    regions.forEach((region, index) => {
      const statusIndicator = region.querySelector('.region-status-indicator');
      const regionName = region.classList[1]; // north-america, europe, etc.
      const continent = document.querySelector(`.continent.${regionName}`);
      
      if (!statusIndicator) return;
      
      // Randomly assign initial states with 60% online, 30% limited, 10% offline
      const randomState = Math.random();
      
      if (randomState < 0.6) {
        // Online state
        statusIndicator.classList.remove('offline', 'limited');
        statusIndicator.classList.add('online');
        statusIndicator.textContent = 'ONLINE';
        statusIndicator.style.backgroundColor = 'rgba(0, 204, 102, 0.15)';
        statusIndicator.style.color = '#00cc66';
        
        if (continent) {
          continent.classList.remove('offline', 'limited');
        }
      } else if (randomState < 0.9) {
        // Limited state
        statusIndicator.classList.remove('offline', 'online');
        statusIndicator.classList.add('limited');
        statusIndicator.textContent = 'LIMITED';
        statusIndicator.style.backgroundColor = 'rgba(255, 204, 0, 0.15)';
        statusIndicator.style.color = '#ffcc00';
        
        if (continent) {
          continent.classList.remove('offline');
          continent.classList.add('limited');
        }
      } else {
        // Offline state
        statusIndicator.classList.remove('online', 'limited');
        statusIndicator.classList.add('offline');
        statusIndicator.textContent = 'OFFLINE';
        statusIndicator.style.backgroundColor = 'rgba(255, 51, 51, 0.15)';
        statusIndicator.style.color = '#ff3333';
        
        if (continent) {
          continent.classList.remove('limited');
          continent.classList.add('offline');
        }
      }
    });
  }

  // Run initial random state setup
  //initializeRegionsWithRandomStates();

  // Create a shuffled array of regions for randomized cascade outage
  const regions = document.querySelectorAll('.region');
  const regionOrder = Array.from(regions);
  for (let i = regionOrder.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [regionOrder[i], regionOrder[j]] = [regionOrder[j], regionOrder[i]];
  }

  // Start the cascading outage after a delay
  setTimeout(() => {
    startCascadingOutage(regionOrder);
  }, 8000);

  function startCascadingOutage(regionOrder) {
    let index = 0;
    const totalRegions = regionOrder.length;
    const outageInterval = (40000) / totalRegions; // Spread over ~40 seconds
    
    function takeDownNextRegion() {
      if (index >= totalRegions) return;
      
      const region = regionOrder[index];
      const statusIndicator = region.querySelector('.region-status-indicator');
      const regionName = region.classList[1]; // north-america, europe, etc.
      const continent = document.querySelector(`.continent.${regionName}`);
      
      if (!statusIndicator) {
        index++;
        setTimeout(takeDownNextRegion, outageInterval);
        return;
      }
      
      // First flicker to limited if not already limited or offline
      if (!statusIndicator.classList.contains('offline')) {
        statusIndicator.classList.remove('online');
        statusIndicator.classList.add('limited');
        statusIndicator.textContent = 'LIMITED';
        statusIndicator.style.backgroundColor = 'rgba(255, 204, 0, 0.15)';
        statusIndicator.style.color = '#ffcc00';
        
        if (continent) {
          continent.classList.remove('online');
          continent.classList.add('limited');
        }
        
        // Then go offline after a short delay
        setTimeout(() => {
          statusIndicator.classList.remove('limited');
          statusIndicator.classList.add('offline');
          statusIndicator.textContent = 'OFFLINE';
          statusIndicator.style.backgroundColor = 'rgba(255, 51, 51, 0.15)';
          statusIndicator.style.color = '#ff3333';
          
          if (continent) {
            continent.classList.remove('limited');
            continent.classList.add('offline');
          }
        }, 1000 + Math.random() * 500);
      }
      
      index++;
      setTimeout(takeDownNextRegion, outageInterval);
    }
    
    takeDownNextRegion();
  }

  // Random region flickering effect (mimics connection attempts)
  function randomRegionFlicker() {
    const regions = document.querySelectorAll('.region');
    
    if (regions.length > 0 && Math.random() > 0.7) {
      const randomRegion = regions[Math.floor(Math.random() * regions.length)];
      const statusIndicator = randomRegion.querySelector('.region-status-indicator');
      const regionName = randomRegion.classList[1]; // north-america, europe, etc.
      const continent = document.querySelector(`.continent.${regionName}`);
      
      // Only flicker regions that are offline
      if (statusIndicator && statusIndicator.classList.contains('offline')) {
        // Briefly show "limited" then back to offline
        statusIndicator.classList.remove('offline');
        statusIndicator.classList.add('limited');
        statusIndicator.textContent = 'LIMITED';
        statusIndicator.style.backgroundColor = 'rgba(255, 204, 0, 0.15)';
        statusIndicator.style.color = '#ffcc00';
        
        if (continent) {
          continent.classList.remove('offline');
          continent.classList.add('limited');
        }
        
        setTimeout(() => {
          statusIndicator.classList.remove('limited');
          statusIndicator.classList.add('offline');
          statusIndicator.textContent = 'OFFLINE';
          statusIndicator.style.backgroundColor = 'rgba(255, 51, 51, 0.15)';
          statusIndicator.style.color = '#ff3333';
          
          if (continent) {
            continent.classList.remove('limited');
            continent.classList.add('offline');
          }
        }, 2000);
      }
    }
    
    setTimeout(randomRegionFlicker, Math.random() * 20000 + 10000);
  }

  // Start random region flickers after the initial cascade
  setTimeout(randomRegionFlicker, 50000);
  
  // Occasionally simulate connection attempt
  function simulateConnectionAttempt() {
    if (Math.random() > 0.7) {
      const reconnectStatus = document.querySelector('.reconnect-status');
      const originalText = reconnectStatus.textContent;
      
      reconnectStatus.textContent = 'CONNECTING...';
      reconnectStatus.style.color = '#ffcc00';
      
      setTimeout(() => {
        reconnectStatus.textContent = originalText;
        reconnectStatus.style.color = '#ffcc00';
      }, 1500);
      
      const reconnectBar = document.querySelector('.reconnect-bar');
      reconnectBar.style.animationDuration = '1s';
      
      setTimeout(() => {
        reconnectBar.style.animationDuration = '3s';
      }, 1500);
    }
    
    setTimeout(simulateConnectionAttempt, Math.random() * 15000 + 10000);
  }
  
  simulateConnectionAttempt();
});