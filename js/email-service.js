// Initialize EmailJS
(function() {
    emailjs.init(EMAIL_CONFIG.jCOTajpd3keVZapOr);
})();

// Email notification service
class EmailNotification {
    static async sendTaskEmail(taskData) {
        const templateParams = {
            to_name: 'Team',
            to_email: EMAIL_CONFIG.DEFAULT_EMAIL,
            task_name: taskData.name,
            task_description: taskData.description,
            assigned_to: taskData.assignedTo || 'Unassigned',
            due_date: taskData.dueDate || 'No deadline',
            priority: taskData.priority || 'Normal',
            dashboard_link: 'https://faadhils.github.io/choremaster-ai/'
        };

        try {
            const response = await emailjs.send(
                EMAIL_CONFIG.SERVICE_ID,
                EMAIL_CONFIG.TEMPLATE_ID,
                templateParams
            );
            console.log('✅ Email sent successfully!', response);
            this.showNotification('Email notification sent!', 'success');
            return true;
        } catch (error) {
            console.error('❌ Email failed:', error);
            this.showNotification('Failed to send email notification', 'error');
            return false;
        }
    }

    static showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 5px;
            color: white;
            background: ${type === 'success' ? '#4CAF50' : '#f44336'};
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}
