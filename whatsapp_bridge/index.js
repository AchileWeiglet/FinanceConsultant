const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

class WhatsAppBridge {
    constructor() {
        this.client = new Client({
            authStrategy: new LocalAuth({
                clientId: "trading-bot"
            })
        });
        
        this.messagesFile = path.join(__dirname, 'messages.json');
        this.outgoingFile = path.join(__dirname, 'outgoing.json');
        
        this.setupEventHandlers();
        this.startOutgoingMessageMonitor();
    }
    
    setupEventHandlers() {
        // QR Code for authentication
        this.client.on('qr', (qr) => {
            console.log('📱 WhatsApp QR Code:');
            console.log('Scan this QR code with your WhatsApp mobile app:');
            qrcode.generate(qr, { small: true });
            console.log('\nAlternatively, you can scan the QR code from the terminal above.');
        });
        
        // Ready event
        this.client.on('ready', () => {
            console.log('✅ WhatsApp client is ready!');
            console.log('🤖 Trading bot is now connected to WhatsApp');
        });
        
        // Authentication events
        this.client.on('authenticated', () => {
            console.log('✅ WhatsApp authentication successful');
        });
        
        this.client.on('auth_failure', (msg) => {
            console.error('❌ WhatsApp authentication failed:', msg);
        });
        
        // Disconnection handling
        this.client.on('disconnected', (reason) => {
            console.log('⚠️ WhatsApp client disconnected:', reason);
        });
        
        // Message handling
        this.client.on('message_create', async (message) => {
            // Only process messages sent TO us (not from us)
            if (!message.fromMe) {
                await this.handleIncomingMessage(message);
            }
        });
        
        this.client.on('message', async (message) => {
            await this.handleIncomingMessage(message);
        });
    }
    
    async handleIncomingMessage(message) {
        try {
            const messageData = {
                id: message.id._serialized,
                from: message.from,
                body: message.body,
                timestamp: message.timestamp,
                type: message.type,
                isGroup: message.from.includes('@g.us')
            };
            
            console.log(`📨 Received message from ${messageData.from}: ${messageData.body}`);
            
            // Skip group messages for now
            if (messageData.isGroup) {
                console.log('⏭️ Skipping group message');
                return;
            }
            
            // Add to messages queue
            await this.addToMessageQueue(messageData);
            
        } catch (error) {
            console.error('❌ Error handling incoming message:', error);
        }
    }
    
    async addToMessageQueue(messageData) {
        try {
            let messages = [];
            
            // Read existing messages
            if (fs.existsSync(this.messagesFile)) {
                const data = fs.readFileSync(this.messagesFile, 'utf8');
                messages = JSON.parse(data);
            }
            
            // Add new message
            messages.push(messageData);
            
            // Write back to file
            fs.writeFileSync(this.messagesFile, JSON.stringify(messages, null, 2));
            
        } catch (error) {
            console.error('❌ Error adding message to queue:', error);
        }
    }
    
    startOutgoingMessageMonitor() {
        // Check for outgoing messages every 2 seconds
        setInterval(async () => {
            await this.processOutgoingMessages();
        }, 2000);
    }
    
    async processOutgoingMessages() {
        try {
            if (!fs.existsSync(this.outgoingFile)) {
                return;
            }
            
            const data = fs.readFileSync(this.outgoingFile, 'utf8');
            const messages = JSON.parse(data);
            
            if (messages.length === 0) {
                return;
            }
            
            // Process each outgoing message
            for (const msg of messages) {
                await this.sendMessage(msg.to, msg.message);
                console.log(`📤 Sent message to ${msg.to}: ${msg.message.substring(0, 50)}...`);
            }
            
            // Clear the outgoing queue
            fs.writeFileSync(this.outgoingFile, JSON.stringify([], null, 2));
            
        } catch (error) {
            console.error('❌ Error processing outgoing messages:', error);
        }
    }
    
    async sendMessage(to, message) {
        try {
            await this.client.sendMessage(to, message);
        } catch (error) {
            console.error(`❌ Error sending message to ${to}:`, error);
        }
    }
    
    async start() {
        console.log('🚀 Starting WhatsApp Trading Bot Bridge...');
        console.log('📱 Please have your phone ready to scan the QR code');
        
        await this.client.initialize();
    }
    
    async stop() {
        console.log('🛑 Stopping WhatsApp client...');
        await this.client.destroy();
    }
}

// Error handling
process.on('unhandledRejection', (err) => {
    console.error('❌ Unhandled promise rejection:', err);
});

process.on('SIGINT', async () => {
    console.log('\n🛑 Received SIGINT, shutting down gracefully...');
    if (bridge) {
        await bridge.stop();
    }
    process.exit(0);
});

// Start the bridge
const bridge = new WhatsAppBridge();
bridge.start().catch(console.error);

console.log('📋 WhatsApp Trading Bot Bridge');
console.log('==============================');
console.log('✅ Bridge is starting...');
console.log('📱 Make sure WhatsApp Web is not open in your browser');
console.log('🔗 You will see a QR code to scan with your phone');
