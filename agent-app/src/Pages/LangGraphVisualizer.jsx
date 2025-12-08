import React, { useState, useEffect, useRef, useLayoutEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
// Terminal UI styles
const terminalStyles = {
  background: '#18181b',
  color: '#39ff14',
  fontFamily: 'monospace',
  fontSize: '1rem',
  borderRadius: '8px',
  padding: '1rem',
  margin: '2rem 1rem',
  minHeight: '180px',
  maxHeight: '300px',
  overflowY: 'auto',
  boxShadow: '0 2px 16px rgba(0,0,0,0.2)',
  border: '1px solid #333',
};
import { Ticket, Bot, Newspaper, Banknote, Activity, ArrowRight, MessageSquare, Send, RefreshCw, AlertCircle, Building2, User, DollarSign } from 'lucide-react';

// Enhanced White Theme Styles
const styles = `
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  .workflow-container {
    width: 100vw;
    height: 100vh;
    background: linear-gradient(135deg, #000000ff 0%, #000000ff 50%, #000000ff 100%);
    color: #333;
    display: flex;
    flex-direction: row;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    overflow: hidden;
    position: relative;
  }

  .workflow-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      radial-gradient(circle at 20% 50%, rgba(4, 0, 60, 1), transparent 50%),
      radial-gradient(circle at 80% 80%, rgba(147, 0, 74, 1), transparent 50%),
      radial-gradient(circle at 40% 20%, rgba(59, 130, 246, 0.3), transparent 50%);
    animation: gradientShift 15s ease infinite;
    pointer-events: none;
  }

  @keyframes gradientShift {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 0.8; transform: scale(1.1); }
  }

  @media (max-width: 768px) {
    .workflow-container {
      flex-direction: column;
    }
  }

  .left-panel {
    flex: 2;
    min-width: 0;
    position: relative;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    height: 100vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  @media (max-width: 768px) {
    .left-panel {
      height: 60vh;
      flex: none;
      border-right: none;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
  }

  .header {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    padding: 1.5rem 2rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    z-index: 10;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  }

  @media (max-width: 480px) {
    .header {
      padding: 1rem 1rem;
    }
  }

  .header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .header-title {
    font-size: 1.5rem;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #ffffff;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  }

  @media (max-width: 480px) {
    .header-title {
      font-size: 1.25rem;
    }
  }

  .header-subtitle {
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.875rem;
    margin-top: 0.25rem;
    font-weight: 500;
  }

  @media (max-width: 480px) {
    .header-subtitle {
      font-size: 0.75rem;
    }
  }

  .connection-status {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.875rem;
    color: #ffffff;
    background: rgba(255, 255, 255, 0.15);
    padding: 0.75rem 1.5rem;
    border-radius: 2rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
  }

  .connection-status:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
  }

  @media (max-width: 480px) {
    .connection-status {
      font-size: 0.75rem;
      padding: 0.5rem 1rem;
    }
  }

  .status-dot {
    width: 0.75rem;
    height: 0.75rem;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.3);
    border: 2px solid rgba(255, 255, 255, 0.5);
    transition: all 0.3s ease;
  }

  .status-connected {
    background-color: #10b981;
    border-color: #10b981;
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.6);
    animation: pulse 2s ease-in-out infinite;
  }

  .status-disconnected {
    background-color: #ef4444;
    border-color: #ef4444;
    box-shadow: 0 0 20px rgba(239, 68, 68, 0.6);
  }

  .workflow-canvas {
    padding: 6rem 2rem 2rem;
    height: 100vh;
    position: relative;
    overflow: auto;
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-template-rows: repeat(3, 1fr);
    gap: 2rem;
    align-items: center;
    justify-items: center;
    background: transparent;
  }

  @media (max-width: 768px) {
    .workflow-canvas {
      height: calc(60vh - 4rem);
      padding: 5rem 1rem 1rem;
      gap: 1.5rem;
    }
  }

  @media (max-width: 480px) {
    .workflow-canvas {
      padding: 5rem 0.5rem 0.5rem;
      gap: 1rem;
    }
  }

  .workflow-node {
    position: relative;
    width: 180px;
    height: 80px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255, 255, 255, 0.2);
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    z-index: 5;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  .workflow-node::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .workflow-node:hover::before {
    opacity: 1;
  }

  @media (max-width: 480px) {
    .workflow-node {
      width: 140px;
      height: 70px;
    }
  }

  .workflow-node.node-active {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.3) 0%, rgba(239, 68, 68, 0.1) 100%);
    border-color: #22c55e;
    border-width: 3px;
    box-shadow: 0 0 40px rgba(34, 197, 94, 0.4), 0 8px 32px rgba(0, 0, 0, 0.2);
    transform: scale(1.05);
    animation: nodeGlow 2s ease-in-out infinite;
  }

  @keyframes nodeGlow {
    0%, 100% { 
      box-shadow: 0 0 40px rgba(34, 197, 94, 0.4), 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    50% { 
      box-shadow: 0 0 60px rgba(34, 197, 94, 0.6), 0 12px 48px rgba(0, 0, 0, 0.3);
    }
  }

  .workflow-node.node-router {
    width: 200px;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
    border-color: rgba(102, 126, 234, 0.5);
  }

  @media (max-width: 480px) {
    .workflow-node.node-router {
      width: 160px;
    }
  }

  .node-content {
    display: flex;
    align-items: center;
    gap: 1rem;
    color: #ffffff;
    position: relative;
    z-index: 2;
  }

  @media (max-width: 480px) {
    .node-content {
      gap: 0.75rem;
    }
  }

  .node-icon {
    width: 2rem;
    height: 2rem;
    padding: 0.4rem;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.2);
    color: #ffffff;
    transition: all 0.3s ease;
  }

  @media (max-width: 480px) {
    .node-icon {
      width: 1.75rem;
      height: 1.75rem;
      padding: 0.3rem;
    }
  }

  .node-icon-active {
    background: rgba(34, 197, 94, 0.3);
    color: #22c55e;
    animation: iconPulse 1.5s ease-in-out infinite;
  }

  @keyframes iconPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
  }

  .node-label {
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    white-space: nowrap;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  @media (max-width: 480px) {
    .node-label {
      font-size: 0.875rem;
    }
  }

  .workflow-node:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.2);
  }

  .workflow-node.node-active:hover {
    transform: translateY(-4px) scale(1.07);
  }

  .node-details {
    position: absolute;
    bottom: 2rem;
    left: 2rem;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 1.5rem;
    padding: 2rem;
    width: 24rem;
    max-width: calc(100vw - 4rem);
    z-index: 20;
    color: #1e293b;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
    animation: slideUp 0.4s ease-out;
  }

  @keyframes slideUp {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
  }

  @media (max-width: 768px) {
    .node-details {
      left: 1rem;
      right: 1rem;
      width: auto;
      max-width: none;
    }
  }

  .details-title {
    font-size: 1.25rem;
    font-weight: 800;
    margin-bottom: 0.75rem;
    color: #0f172a;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .details-description {
    color: #475569;
    font-size: 0.95rem;
    margin-bottom: 1rem;
    line-height: 1.6;
  }

  .details-code {
    font-size: 0.85rem;
    color: #64748b;
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
    padding: 1rem;
    border-radius: 0.75rem;
    white-space: pre-wrap;
    font-family: 'Monaco', 'Courier New', monospace;
    border: 1px solid #cbd5e1;
    line-height: 1.5;
  }

  .right-panel {
    width: 35vw;
    min-width: 320px;
    max-width: 550px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    display: flex;
    border-left: 2px solid rgba(255, 255, 255, 1);
    flex-direction: column;
    box-shadow: -8px 0 40px rgba(0, 0, 0, 0.1);
    z-index: 2;
    padding: 2rem 0 0 0;
    height: 100vh;
    overflow: hidden;
  }

  @media (max-width: 768px) {
    .right-panel {
      width: 100vw;
      min-width: 100%;
      max-width: 100%;
      height: 40vh;
      border-left: none;
      border-top: 1px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 -8px 40px rgba(0, 0, 0, 0.1);
      padding-top: 1rem;
    }
  }

  .chat-header {
    padding: 0 2rem 1.5rem 2rem;
    border-bottom: none;
    background: transparent;
  }

  @media (max-width: 480px) {
    .chat-header {
      padding: 0 1rem 1rem 1rem;
    }
  }

  .chat-title {
    font-size: 1.25rem;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #ffffff;
    margin-bottom: 0.25rem;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  }

  .chat-subtitle {
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.95rem;
    margin-top: 0.25rem;
    font-weight: 500;
  }

  .messages-container {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 1.5rem 1rem;
    display: flex;
    flex-direction: column;
    border-radius: 0.25rem;
    gap: 1.25rem;
    background: transparent;
    box-shadow: inset 0 2px 20px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    margin: 0 1rem;
    scroll-behavior: smooth;
  }

  @media (max-width: 480px) {
    .messages-container {
      padding: 1rem;
      gap: 1rem;
      margin: 0 0.5rem;
    }
  }

  .messages-container::-webkit-scrollbar {
    width: 8px;
  }

  .messages-container::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
  }

  .messages-container::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 10px;
  }

  .messages-container::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.3);
  }

  .empty-state {
    text-align: center;
    color: rgba(255, 255, 255, 0.8);
    padding: 3rem 1rem;
  }

  .empty-icon {
    width: 3.5rem;
    height: 3.5rem;
    margin: 0 auto 1rem;
    opacity: 0.6;
    color: #ffffff;
    animation: float 3s ease-in-out infinite;
  }

  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
  }

  .message-wrapper {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    animation: messageSlide 0.4s ease-out;
    width: 100%;
  }

  @keyframes messageSlide {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .message-user {
    flex-direction: row-reverse;
    justify-content: flex-end;
  }

  .message-bot {
    justify-content: flex-start;
    flex-direction: row;
  }

  .message-avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.3) 0%, rgba(255, 255, 255, 0.1) 100%);
    border: 2px solid rgba(255, 255, 255, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    color: #ffffff;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    flex-shrink: 0;
  }

  .message-bubble {
    flex: 1;
    max-width: calc(100% - 60px);
    padding: 1.25rem 1.5rem;
    border-radius: 1rem;
    font-size: 0.95rem;
    line-height: 1.7;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(10px);
    margin-bottom: 2px;
    word-wrap: break-word;
    overflow-wrap: break-word;
  }

  @media (max-width: 480px) {
    .message-bubble {
      max-width: calc(100% - 50px);
      padding: 1rem 1.25rem;
      font-size: 0.875rem;
    }
  }

  .bubble-user {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-top-right-radius: 0.5rem;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .bubble-bot {
    background: rgba(255, 255, 255, 0.98);
    color: #1e293b;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-top-left-radius: 0.5rem;
    max-height: none;
  }

  .bubble-error {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
    color: #ffffff;
    border: 1px solid rgba(239, 68, 68, 0.4);
    border-radius: 1.25rem;
  }

  .message-meta {
    font-size: 0.75rem;
    color: #64748b;
    margin-bottom: 0.5rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .loading-message {
    display: flex;
    justify-content: flex-start;
  }

  .loading-bubble {
    background: rgba(255, 255, 255, 0.2);
    display: none;
    color: #ffffff;
    padding: 1rem;
    margin: 0.25rem;
    border-radius: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(10px);
  }

  .loading-content {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .loading-spinner {
    width: 1.25rem;
    height: 1.25rem;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid #ffffff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .input-container {
    padding: 1.5rem 2rem 2rem 2rem;
    border-top: none;
    background: transparent;
  }

  @media (max-width: 480px) {
    .input-container {
      padding: 1rem 1rem 1.5rem 1rem;
    }
  }

  .input-row {
    display: flex;
    gap: 1rem;
    align-items: center;
    background: transparent;
    border-radius: 0.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    padding: 0.5rem;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    transition: all 0.3s ease;
    flex-shrink: 0;
  }

  .input-row:focus-within {
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  }

  .message-input {
    flex: 1;
    padding: 1rem 1.5rem;
    background: transparent;
    border: none;
    color: #ffffffff;
    font-size: 1rem;
    outline: none;
    transition: all 0.3s ease;
  }

  .message-input::placeholder {
    color: rgba(255, 255, 255, 0.6);
  }

  .message-input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .send-button {
    padding: 0.8rem;
    margin: 0.2rem;
    min-width: 50px;
    background: linear-gradient(135deg, rgba(71, 0, 59, 1) 0%, rgba(0, 0, 0, 0.53) 100%);
    border: 2px solid rgba(255, 255, 255, 0.55);
    border-radius: 5rem;
    color: #ffffffff;C
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }

  .send-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0.3) 100%);
  }

  .send-button:active:not(:disabled) {
    transform: scale(0.95);
  }

  .send-button:disabled {
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.4);
    cursor: not-allowed;
    box-shadow: none;
  }

  .skeleton-loader {
    background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.15) 50%, rgba(255, 255, 255, 0.05) 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 0.75rem;
  }

  @keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }

  .skeleton-text {
    height: 1rem;
    margin-bottom: 0.5rem;
  }

  .skeleton-text-short {
    width: 60%;
  }

  .error-banner {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
    border: 2px solid rgba(239, 68, 68, 0.5);
    border-radius: 1rem;
    padding: 1.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    animation: slideDown 0.3s ease-out;
  }

  @keyframes slideDown {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .error-content {
    flex: 1;
  }

  .error-title {
    font-weight: 700;
    color: #ef4444;
    margin-bottom: 0.5rem;
    font-size: 1rem;
  }

  .error-message {
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.875rem;
  }

  .retry-button {
    background: rgba(239, 68, 68, 0.2);
    border: 1px solid rgba(239, 68, 68, 0.5);
    color: #ef4444;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .retry-button:hover {
    background: rgba(239, 68, 68, 0.3);
    transform: translateY(-2px);
  }

  .markdown-content {
    line-height: 1.8;
    width: 100%;
  }

  .markdown-content h1,
  .markdown-content h2,
  .markdown-content h3,
  .markdown-content h4 {
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
    line-height: 1.3;
  }

  .markdown-content h1 { font-size: 1.5rem; }
  .markdown-content h2 { font-size: 1.25rem; }
  .markdown-content h3 { font-size: 1.1rem; }
  .markdown-content h4 { font-size: 1rem; }

  .markdown-content p {
    margin-bottom: 0.75rem;
  }

  .markdown-content code {
    background: rgba(0, 0, 0, 0.2);
    padding: 0.2rem 0.5rem;
    border-radius: 0.3rem;
    font-family: 'Monaco', 'Courier New', monospace;
    font-size: 0.875em;
    border: 1px solid rgba(0, 0, 0, 0.1);
  }

  .markdown-content pre {
    background: rgba(0, 0, 0, 0.3);
    padding: 1rem;
    border-radius: 0.5rem;
    overflow-x: auto;
    margin: 0.75rem 0;
    border: 1px solid rgba(0, 0, 0, 0.2);
  }

  .markdown-content pre code {
    background: transparent;
    padding: 0;
    border: none;
  }

  .markdown-content ul, .markdown-content ol {
    margin-left: 1.5rem;
    margin-bottom: 0.75rem;
    padding-left: 0.5rem;
  }

  .markdown-content li {
    margin-bottom: 0.25rem;
  }

  .markdown-content blockquote {
    border-left: 3px solid rgba(0, 0, 0, 0.3);
    padding-left: 1rem;
    margin: 0.75rem 0;
    font-style: italic;
    opacity: 0.9;
  }

  .markdown-content strong {
    font-weight: 700;
  }

  .markdown-content em {
    font-style: italic;
  }

  #terminal-output {
    scrollbar-width: thin;
    scrollbar-color: #ffffffff rgba(0, 0, 0, 0.3);
  }

  #terminal-output::-webkit-scrollbar {
    width: 12px !important;
  }

  #terminal-output::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.5) !important;
    border-radius: 10px !important;
    margin: 0.5rem 0 !important;
  }

  #terminal-output::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #1eff00ff 0%, #000000ff 100%) !important;
    border-radius: 10px !important;
    box-shadow: 0 0 15px 1eff00ff !important;
    min-height: 40px !important;
  }

  #terminal-output::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #1eff00ff 0%, #00e5ff 100%) !important;
    box-shadow: 0 0 25px rgba(0, 255, 135, 1) !important;
  }

  #terminal-output::-webkit-scrollbar-thumb:active {
    background: linear-gradient(180deg, #1eff00ff 0%, #00ffff 100%) !important;
    box-shadow: 0 0 30px rgba(0, 255, 135, 1) !important;
  }

  .terminal-container::-webkit-scrollbar {
    width: 12px;
  }

  .terminal-container::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 10px;
    margin: 0.5rem 0;
  }

  .terminal-container::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00ff87 0%, #00c8ff 100%);
    border-radius: 10px;
    border: none;
    box-shadow: 0 0 15px rgba(0, 255, 135, 0.6), inset 0 0 10px rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    min-height: 40px;
  }

  .terminal-container::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #00ffaa 0%, #00e5ff 100%);
    box-shadow: 0 0 25px rgba(0, 255, 135, 0.8), inset 0 0 10px rgba(255, 255, 255, 0.15);
  }

  .terminal-container::-webkit-scrollbar-thumb:active {
    background: linear-gradient(180deg, #00ffcc 0%, #00ffff 100%);
    box-shadow: 0 0 30px rgba(0, 255, 135, 1), inset 0 0 15px rgba(255, 255, 255, 0.2);
  }

  .execution-status {
    position: absolute;
    top: 7rem;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(20px);
    color: #ffffff;
    padding: 1rem 2rem;
    border-radius: 2rem;
    z-index: 20;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    font-weight: 600;
    animation: statusFade 0.4s ease-out;
  }

  @keyframes statusFade {
    from { opacity: 0; transform: translateX(-50%) translateY(-10px); }
    to { opacity: 1; transform: translateX(-50%) translateY(0); }
  }

  @media (max-width: 768px) {
    .execution-status {
      top: 5rem;
      padding: 0.75rem 1.5rem;
      font-size: 0.875rem;
    }
  }

  .status-indicator {
    width: 0.75rem;
    height: 0.75rem;
    background-color: #22c55e;
    border-radius: 50%;
    animation: pulse 1.5s ease-in-out infinite;
    box-shadow: 0 0 20px rgba(34, 197, 94, 0.6);
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(0.9); }
  }

  .metrics-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.5rem;
    background: rgba(34, 197, 94, 0.1);
    border-radius: 0.5rem;
    font-size: 0.75rem;
    color: #22c55e;
    font-weight: 600;
  }`;

// Insert styles into document
if (typeof document !== 'undefined') {
  const styleSheet = document.createElement('style');
  styleSheet.textContent = styles;
  document.head.appendChild(styleSheet);
}



const LangGraphVisualizer = () => {
  // Terminal output state
  const [terminalOutput, setTerminalOutput] = useState('');
  const [terminalConnected, setTerminalConnected] = useState(null);

  // Clear terminal on page refresh and check connection
  useEffect(() => {
    setTerminalOutput('');
    checkConnection();
  }, []);

  // Fetch terminal output from backend (plain text)
  useEffect(() => {
    const fetchTerminalOutput = async () => {
      try {
        const response = await fetch('http://localhost:8000/terminal-output');
        if (!response.ok) {
          setTerminalConnected(false);
          setIsConnected(false);
          return;
        }
        setTerminalConnected(true);
        setIsConnected(true);
        setConnectionError(null);
      } catch {
        setTerminalConnected(false);
        setIsConnected(false);
      }
    };
    // Only check connection, don't fetch/display backend terminal output
    const interval = setInterval(fetchTerminalOutput, 5000);
    return () => clearInterval(interval);
  }, []);
  const [selectedNode, setSelectedNode] = useState(null);
  const [executionPath, setExecutionPath] = useState([]);
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [connectionError, setConnectionError] = useState(null);
  const messagesEndRef = useRef(null);
  // Responsive node refs and layout effect
  const canvasRef = useRef(null);
  // Node definitions matching your Python LangGraph structure (positions removed for grid alignment)
  const nodes = [
    {
      id: 'router',
      type: 'router',
      label: 'Agentic Ai',
      icon: Bot,
      description: 'Routes user input using OpenAI Chat',
      details: 'Function: router_node()\nDecides which agent handles the query',
    },
    {
      id: 'ticket_analyzer',
      type: 'agent',
      label: 'Ticket Analyzer',
      icon: Ticket,
      description: 'Handles tickets raised by employees, players, or parents',
      details: 'Function: ticket_analyzer_node()\nCapabilities: Ticket management, status tracking',
    },
    {
      id: 'news_aggregator',
      type: 'agent',
      label: 'News and Announcements',
      icon: Newspaper,
      description: 'Collects latest news articles using newsdata.io API',
      details: 'Function: news_aggregator_node()\nCapabilities: News fetching, article aggregation',
    },
    {
      id: 'activity_tracker',
      type: 'agent',
      label: 'Activity Tracker',
      icon: Activity,
      description: 'Tracks employee activities like a Kanban board',
      details: 'Function: activity_tracker_node()\nCapabilities: Task tracking, Kanban view',
    },
    {
      id: 'infrastructure_cost_monitor',
      type: 'agent',
      label: 'Infrastructure Cost Monitor',
      icon: Banknote,
      description: 'Monitors cloud infrastructure costs (AWS, Azure, GCP, Firebase, etc.)',
      details: 'Function: infrastructure_cost_monitor_node()\nCapabilities: Cloud cost tracking, pricing comparison',
    },
    {
      id: 'chat',
      type: 'agent',
      label: 'Chat Agent',
      icon: Building2,
      description: 'General conversation and Technology-Garage company information',
      details: 'Function: chat_node()\nCapabilities: General chat, company info',
    },
  ];
  // Create refs for each node
  const nodeRefs = React.useMemo(() => {
    const refs = {};
    nodes.forEach(n => { refs[n.id] = refs[n.id] || React.createRef(); });
    return refs;
  }, [nodes.length]);
  // Re-render on resize for SVG lines
  const [, forceUpdate] = useState(0);
  useLayoutEffect(() => {
    const handleResize = () => forceUpdate(n => n + 1);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Scroll to bottom on messages update
  useEffect(() => {
    if (messagesEndRef.current) {
      // Use setTimeout to ensure DOM has updated before scrolling
      setTimeout(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
      }, 0);
    }
  }, [messages, isLoading]);

  // Check backend connection
  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      const response = await fetch('http://localhost:8000/health');
      if (response.ok) {
        setIsConnected(true);
        setConnectionError(null);
      } else {
        setIsConnected(false);
        setConnectionError('Backend server returned an error');
      }
    } catch (error) {
      setIsConnected(false);
      setConnectionError('Cannot connect to backend server at localhost:8000');
    }
  };

  const retryConnection = () => {
    setConnectionError(null);
    checkConnection();
  };



  const connections = [
    { from: 'router', to: 'ticket_analyzer', condition: 'TicketAnalyzerAgent' },
    { from: 'router', to: 'news_aggregator', condition: 'NewsAggregatorAgent' },
    { from: 'router', to: 'activity_tracker', condition: 'ActivityTrackerAgent' },
    { from: 'router', to: 'infrastructure_cost_monitor', condition: 'InfrastructureCostMonitorAgent' },
    { from: 'router', to: 'chat', condition: 'ChatAgent' },
  ];

  // Send message to Python backend
  const sendMessage = async () => {
    if (!userInput.trim() || !isConnected) return;

    setIsLoading(true);
    setExecutionPath([]); // All gray initially

    const newMessage = { type: 'user', content: userInput };
    setMessages(prev => [...prev, newMessage]);

    // Show immediate loading message in chat
    setMessages(prev => [
      ...prev,
      {
        type: 'bot',
        content: '',
        isLoading: true
      }
    ]);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput })
      });

      const data = await response.json();
      // Parse all agent names from query_type (comma-separated)
      const agentNames = (data.query_type || '').split(',').map(a => a.trim()).filter(Boolean);
      const agentNameToNodeId = {
        'TicketAnalyzerAgent': 'ticket_analyzer',
        'NewsAggregatorAgent': 'news_aggregator',
        'ActivityTrackerAgent': 'activity_tracker',
        'InfrastructureCostMonitorAgent': 'infrastructure_cost_monitor',
        'ChatAgent': 'chat',
        'ticket_analyzer': 'ticket_analyzer',
        'news_aggregator': 'news_aggregator',
        'activity_tracker': 'activity_tracker',
        'infrastructure_cost_monitor': 'infrastructure_cost_monitor',
        'chat': 'chat',
      };
      let agentResponses = {};
      let hasAgentResponses = typeof data.agent_responses === 'object' && data.agent_responses !== null;
      if (hasAgentResponses) {
        agentResponses = data.agent_responses;
      }
      // Always use the summary field from backend for chat display
      let summaryContent = data.summary || data.response || 'No response';
      
      // Animate router, then each agent one by one
      let delay = 0;
      setExecutionPath([]); // All gray
      setTimeout(() => setExecutionPath(['router']), delay += 800); // router active
      agentNames.forEach((agent, idx) => {
        const nodeId = agentNameToNodeId[agent] || agent.toLowerCase();
        setTimeout(() => setExecutionPath(['router', nodeId]), delay += 1200);
        setTimeout(() => setExecutionPath(['router']), delay += 800);
      });
      
      const totalAnimationTime = delay + 800; // Total time for all animations

      // Show all agent responses in terminal AFTER visualization completes
      setTimeout(() => {
        let terminalContent = '';
        let allResponses = '';
        let uniqueResponses = new Set();
        
        // Build terminal header
        terminalContent += agentNames.length > 0
          ? `Invoking agents: ${agentNames.join(', ')}\n\n`
          : '';
        
        // Collect all agent responses
        let responseBlocks = [];
        if (hasAgentResponses && Object.keys(agentResponses).length > 0) {
          Object.entries(agentResponses).forEach(([agent, resp], idx, arr) => {
            responseBlocks.push({ agent, resp });
          });
        }
        
        // Show agent responses (but not the summary to avoid duplication)
        responseBlocks.forEach(({ agent, resp }, idx) => {
          if (!uniqueResponses.has(resp)) {
            allResponses += `\n[${agent} is answering...]\n--- ${agent} ---\n${resp}\n`;
            uniqueResponses.add(resp);
          }
        });
        
        // Add summary at the end only if it's different from agent responses
        if (summaryContent && !uniqueResponses.has(summaryContent)) {
          allResponses += `\n${summaryContent}`;
        }
        
        // Update terminal with all content at once
        setTerminalOutput(terminalContent + allResponses);
        setExecutionPath([]);
      }, totalAnimationTime);
      
      // Show response in chat AFTER terminal output (with delay for visibility)
      setTimeout(() => {
        setMessages(prev => {
          const updated = [...prev];
          // Find and update the last loading message
          for (let i = updated.length - 1; i >= 0; i--) {
            if (updated[i]?.isLoading) {
              updated[i] = {
                ...updated[i],
                content: summaryContent,
                isLoading: false
              };
              break;
            }
          }
          return updated;
        });
        setIsLoading(false);
      }, totalAnimationTime + 500);
    } catch (error) {
      const errorMessage = { 
        type: 'error', 
        content: 'Failed to connect to Python backend. Make sure your server is running on localhost:8000',
        canRetry: true
      };
      setMessages(prev => [...prev, errorMessage]);
      setIsLoading(false);
      setConnectionError('Connection failed during message send');
    }

    setUserInput('');
  };

  const retryMessage = (messageIndex) => {
    const message = messages[messageIndex - 1];
    if (message && message.type === 'user') {
      setUserInput(message.content);
      setTimeout(() => sendMessage(), 100);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      // Keep input focused during send to prevent layout shift
      const inputElement = e.target;
      sendMessage();
      // Restore focus after message sent
      setTimeout(() => {
        inputElement?.focus();
      }, 100);
    }
  };

  // Connection-related functions removed for better responsiveness

  return (
    <div className="workflow-container" style={{ position: 'relative', height: '100vh', overflow: 'hidden' }}>
      {/* Left Panel - Workflow Visualization and Terminal stacked */}
      <div className="left-panel" style={{ display: 'flex', flexDirection: 'column', height: '100vh', overflow: 'hidden' }}>
        {/* Header */}
        <div className="header">
          <div className="header-content">
            <div>
              <h1 className="header-title">
                Agentic AI 
              </h1>
              <p className="header-subtitle" style={{ fontSize: 12, textAlign: 'right' }}>by Technology Garage</p>
            </div>
            <div className="connection-status">
              <div className={`status-dot ${isConnected ? 'status-connected' : 'status-disconnected'}`}></div>
              <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
            </div>
          </div>
        </div>


        {/* Responsive Workflow Canvas using CSS Grid (75vh) */}
        <div
          className="workflow-canvas"
          style={{
            height: '75vh',
            width: '100%',
            marginTop: '50px',
            position: 'relative',
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gridTemplateRows: 'repeat(3, 1fr)',
            alignItems: 'center',
            justifyItems: 'center',
            overflow: 'auto',
          }}
          ref={canvasRef}
        >
          {/* SVG Connections (drawn after layout) */}
          <svg
            width="100%"
            height="100%"
            style={{ position: 'absolute', top: 0, left: 0, pointerEvents: 'none', zIndex: 0 }}
          >
            {Object.entries(nodeRefs).length > 1 &&
              nodes.filter(n => n.id !== 'router').map((node) => {
                const fromRef = nodeRefs['router'];
                const toRef = nodeRefs[node.id];
                if (!fromRef.current || !toRef.current || !canvasRef.current) return null;
                const fromRect = fromRef.current.getBoundingClientRect();
                const toRect = toRef.current.getBoundingClientRect();
                const canvasRect = canvasRef.current.getBoundingClientRect();
                // Start from center of router node
                const x1 = fromRect.left + fromRect.width / 2 - canvasRect.left;
                const y1 = fromRect.top + fromRect.height / 2 - canvasRect.top;
                // End at center of agent node
                const x2 = toRect.left + toRect.width / 2 - canvasRect.left;
                const y2 = toRect.top + toRect.height / 2 - canvasRect.top;
                const isActive = executionPath.includes(node.id);
                return (
                  <line
                    key={node.id}
                    x1={x1}
                    y1={y1}
                    x2={x2}
                    y2={y2}
                    stroke={isActive ? '#22c55e' : '#ffffffff'}
                    strokeWidth={isActive ? 4 : 3}
                    strokeDasharray={isActive ? '8 6' : '6 6'}
                    style={{ opacity: isActive || executionPath.includes('router') ? 1 : 0.7, transition: 'stroke 0.3s'}}
                  />
                );
              })}
          </svg>

          {/* Nodes in grid cells, responsive */}
          {nodes.map((node, idx) => {
            const IconComponent = node.icon;
            const isActive = executionPath.includes(node.id);
            // Grid placement: cleaner 5-agent layout
            const gridArea = {
              'router': { gridColumn: 3, gridRow: 2 },
              'ticket_analyzer': { gridColumn: 1, gridRow: 1 },
              'news_aggregator': { gridColumn: 3, gridRow: 1 },
              'activity_tracker': { gridColumn: 5, gridRow: 1 },
              'infrastructure_cost_monitor': { gridColumn: 2, gridRow: 3 },
              'chat': { gridColumn: 4, gridRow: 3 },
            }[node.id] || { gridColumn: 3, gridRow: 2 };
            // Cleaner, modern color scheme
            const nodeGradients = {
              router: 'rgba(0, 146, 165, 1)', // Blue
              ticket_analyzer: 'rgba(132, 0, 255, 1)', // Purple
              news_aggregator: 'rgba(143, 0, 107, 1)', // Red
              activity_tracker: 'rgba(0, 102, 68, 1)', // Green
              infrastructure_cost_monitor: 'rgba(187, 118, 0, 1)', // Amber
              chat: 'rgba(0, 43, 112, 1)', // Light blue
            };
            let nodeStyle = {
              gridColumn: gridArea.gridColumn,
              gridRow: gridArea.gridRow,
              width: node.id === 'router' ? 280 : 180,
              height: node.id === 'router' ? 100 : 90,
              padding: '16px',
              background: isActive ? 'rgba(255, 255, 255, 1)' : nodeGradients[node.id],
              color: isActive ? '#000000ff' : '#e2e8f0',
              borderRadius: 12,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 600,
              fontSize: node.id === 'router' ? 18 : 14,
              boxShadow: isActive ? '0 0 24px rgba(59, 130, 246, 0.5), 0 4px 16px rgba(0, 0, 0, 0.3)' : '0 4px 16px rgba(0, 0, 0, 0.3)',
              border: isActive ? '2px solid #3b82f6' : '2px solid rgba(148, 163, 184, 0.3)',
              cursor: 'pointer',
              opacity: 1,
              transition: 'all 0.3s',
              position: 'relative',
              zIndex: isActive ? 10 : 2,
            };
            return (
              <div
                key={node.id}
                ref={nodeRefs[node.id]}
                style={nodeStyle}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 15 }}>
                  <IconComponent style={{ width: 30, height: 30, color: isActive ? '#000000ff' : '#ffffffff' }} />
                  <span>{node.label}</span>
                </div>
              </div>
            );
          })}

            {/* Node Details - Hidden */}
            {false && selectedNode && (
              <div className="node-details" style={{ left: 350, top: 500, position: 'absolute', zIndex: 20 }}>
                <h3 className="details-title">
                  {nodes.find(n => n.id === selectedNode)?.label}
                </h3>
                <p className="details-description">
                  {nodes.find(n => n.id === selectedNode)?.description}
                </p>
                <pre className="details-code">
                  {nodes.find(n => n.id === selectedNode)?.details}
                </pre>
              </div>
            )}

            {/* Execution Status */}
            {executionPath.length > 0 && (
              <div className="execution-status">
                <div className="status-indicator"></div>
                Executing workflow...
              </div>
            )}
        </div>
        {/* Terminal Output Overlay (40vh, bottom) */}
        <div id="terminal-output" className="terminal-container" style={{
          height: '25vh',
          background: 'linear-gradient(135deg, #0a0a0aff 0%, #1a0a1aff 50%, #0a0a0aff 100%)',
          color: '#ffffffff',
          fontFamily: 'monospace',
          fontSize: '0.95rem',
          borderTop: '2px solid #ffffffff',
          boxShadow: 'inset 0 2px 20px rgba(0, 255, 135, 0.05), 0 -2px 16px rgba(0,0,0,0.4)',
          zIndex: 10,
          padding: '1.25rem',
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
        }}>
          <div style={{ fontWeight: 700, marginBottom: '0rem', color: '#ae00ffff', fontSize: '0.95rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingBottom: '0.2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              Terminal Output
            </div>
            <div style={{ color: terminalConnected === true ? '#00ff87ff' : '#ff3333ff', fontWeight: 600, fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: terminalConnected === true ? '#00ff87' : '#ff3333', boxShadow: terminalConnected === true ? '0 0 8px #00ff87' : '0 0 8px #ff3333' }}></span>
              {terminalConnected === true && 'Connected'}
              {terminalConnected === false && 'Disconnected'}
            </div>
          </div>
          {/* Syntax-highlighted terminal output */}
          {terminalOutput && (
            <div style={{ marginTop: '0.5rem', flex: 1, overflowY: 'auto', lineHeight: '1.6' }}>
              {terminalOutput.split('\n').map((line, idx) => {
                let lineColor = '#b0b0b0';
                let fontWeight = '400';
                let textShadow = 'none';
                
                if (line.includes('Thinking...')) {
                  lineColor = '#fbbf24';
                  fontWeight = '600';
                  textShadow = '0 0 8px rgba(251, 191, 36, 0.3)';
                } else if (line.includes('Invoking agents:')) {
                  lineColor = '#00d9ff';
                  fontWeight = '600';
                  textShadow = '0 0 8px rgba(0, 217, 255, 0.4)';
                } else if (line.includes('---') && line.includes('Agent')) {
                  lineColor = '#00ff87';
                  fontWeight = '700';
                  textShadow = '0 0 10px rgba(0, 255, 135, 0.5)';
                } else if (line.toLowerCase().includes('error') || line.includes('[400]')) {
                  lineColor = '#ff3333';
                  fontWeight = '700';
                  textShadow = '0 0 8px rgba(255, 51, 51, 0.4)';
                } else if (line.includes('is answering')) {
                  lineColor = '#d084ff';
                  fontWeight = '600';
                  textShadow = '0 0 8px rgba(208, 132, 255, 0.3)';
                } else if (line.trim() === '') {
                  return <div key={idx} style={{ height: '0.5rem' }} />;
                }
                
                return (
                  <div key={idx} style={{ color: lineColor, marginBottom: '0.35rem', lineHeight: '1.5', fontWeight, textShadow, fontFamily: "'Fira Code', 'Courier New', monospace" }}>
                    {line || ' '}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Right Panel - Chat Interface */}
      <div className="right-panel">
        {/* Chat Header */}
        <div className="chat-header">
          <h2 className="chat-title">
            <MessageSquare className="w-5 h-5" />
            Live Chat
          </h2>
          <p className="chat-subtitle">LangGraph</p>
        </div>

        {/* Messages */}
        <div className="messages-container">
          {connectionError && (
            <div className="error-banner">
              <AlertCircle size={24} color="#ef4444" />
              <div className="error-content">
                <div className="error-title">Connection Error</div>
                <div className="error-message">{connectionError}</div>
              </div>
              <button className="retry-button" onClick={retryConnection}>
                <RefreshCw size={16} />
                Retry
              </button>
            </div>
          )}
          {messages.length === 0 && (
            <div className="empty-state">
              <Activity className="empty-icon" />
              <p>{connectionError ? 'Waiting for connection...' : 'Start chatting to see the workflow in action!'}</p>
            </div>
          )}
          {messages.map((msg, idx) => (
            <div key={idx} className={`message-wrapper ${msg.type === 'user' ? 'message-user' : 'message-bot'}`}>
              <div className="message-avatar">
                {msg.type === 'user' ? <User size={22} /> : msg.type === 'error' ? <AlertCircle size={22} /> : <Bot size={22} />}
              </div>
              <div className={`message-bubble ${
                msg.type === 'user' ? 'bubble-user' : 
                msg.type === 'error' ? 'bubble-error' : 'bubble-bot'
              }`}>
                {/* Show 'Response' label for LLM router */}
                {msg.type === 'bot' && (
                  <div style={{ fontWeight: 700, color: msg.isLoading ? '#00626eff' : '#22c55e', marginBottom: 8, fontSize: '0.95rem' }}>
                    {msg.isLoading ? 'Thinking...' : ' Response'}
                  </div>
                )}
                {msg.type === 'error' && msg.canRetry && (
                  <button 
                    className="retry-button" 
                    onClick={() => retryMessage(idx)}
                    style={{ marginTop: '0.5rem' }}
                  >
                    <RefreshCw size={14} />
                    Retry
                  </button>
                )}
                {/* Render markdown for bot messages */}
                {msg.type === 'bot' ? (
                  !msg.isLoading && (
                    <div className="markdown-content">
                      <ReactMarkdown
                        components={{
                        code({node, inline, className, children, ...props}) {
                          const match = /language-(\w+)/.exec(className || '');
                          return !inline && match ? (
                            <SyntaxHighlighter
                              style={vscDarkPlus}
                              language={match[1]}
                              PreTag="div"
                              {...props}
                            >
                              {String(children).replace(/\n$/, '')}
                            </SyntaxHighlighter>
                          ) : (
                            <code className={className} {...props}>
                              {children}
                            </code>
                          );
                        }
                      }}
                    >
                      {msg.content}
                    </ReactMarkdown>
                    </div>
                  )
                ) : (
                  <p>{msg.content}</p>
                )}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="input-container">
          <div className="input-row">
            <input
              className="message-input"
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={isConnected ? "Ask me anything..." : "Backend not connected"}
              disabled={!isConnected || isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={!isConnected || isLoading || !userInput.trim()}
              className="send-button"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
          
        </div>
      </div>
    </div>
  );
};

export default LangGraphVisualizer;