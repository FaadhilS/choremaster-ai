// Task creation with email notification
async function createTask() {
    const taskData = {
        name: document.getElementById('taskName').value,
        description: document.getElementById('taskDescription').value,
        assignedTo: document.getElementById('assignedTo').value,
        dueDate: document.getElementById('dueDate').value,
        priority: document.getElementById('priority').value,
        createdAt: new Date().toISOString()
    };

    // Validate task data
    if (!taskData.name) {
        alert('Please enter a task name');
        return;
    }

    // Save task to local storage
    saveTaskLocally(taskData);
    
    // Send email if checkbox is checked
    if (document.getElementById('sendEmail').checked) {
        await EmailNotification.sendTaskEmail(taskData);
    }
    
    // Update UI
    displayTask(taskData);
    clearForm();
}

function saveTaskLocally(task) {
    let tasks = JSON.parse(localStorage.getItem('tasks') || '[]');
    tasks.push(task);
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function displayTask(task) {
    const taskList = document.getElementById('taskList');
    const taskElement = document.createElement('div');
    taskElement.className = 'task-item';
    taskElement.innerHTML = `
        <h3>${task.name}</h3>
        <p>${task.description}</p>
        <small>Assigned to: ${task.assignedTo || 'Unassigned'}</small>
        <small>Due: ${task.dueDate || 'No deadline'}</small>
        <span class="priority-${task.priority.toLowerCase()}">${task.priority}</span>
    `;
    taskList.appendChild(taskElement);
}

function clearForm() {
    document.getElementById('taskName').value = '';
    document.getElementById('taskDescription').value = '';
    document.getElementById('assignedTo').value = '';
    document.getElementById('dueDate').value = '';
    document.getElementById('priority').value = 'Normal';
}
