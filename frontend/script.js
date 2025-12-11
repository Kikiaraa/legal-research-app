// API基础URL - 自动检测环境
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5001/api'
    : '/api';

// 全局变量
let questions = {};
let jurisdictions = [];
let selectedQuestions = new Set();
let selectedJurisdiction = '';

// DOM元素
const customJurisdictionSelect = document.getElementById('customJurisdictionSelect');
const selectDisplay = customJurisdictionSelect.querySelector('.select-display');
const selectText = customJurisdictionSelect.querySelector('.select-text');
const selectOptions = document.getElementById('jurisdictionOptions');
const questionsContainer = document.getElementById('questionsContainer');
const generateBtn = document.getElementById('generateReport');
const resultsSection = document.getElementById('resultsSection');
const reportHeader = document.getElementById('reportHeader');
const reportContent = document.getElementById('reportContent');

// 初始化应用
async function initApp() {
    console.log('开始初始化应用');
    try {
        console.log('加载问题和司法辖区数据');
        await Promise.all([loadQuestions(), loadJurisdictions()]);
        console.log('数据加载完成，设置事件监听器');
        setupEventListeners();
        console.log('应用初始化成功');
    } catch (error) {
        console.error('初始化失败:', error);
        showError(`应用初始化失败: ${error.message}`);
    }
}

// 加载问题列表
async function loadQuestions() {
    try {
        const response = await fetch(`${API_BASE_URL}/questions`);
        if (!response.ok) {
            throw new Error(`获取问题列表失败: ${response.status}`);
        }
        
        const text = await response.text();
        if (!text) {
            throw new Error('服务器返回空响应');
        }
        
        questions = JSON.parse(text);
        renderQuestions();
    } catch (error) {
        console.error('加载问题失败:', error);
        showError(`加载问题列表失败: ${error.message}`);
    }
}

// 加载司法辖区列表
async function loadJurisdictions() {
    try {
        const response = await fetch(`${API_BASE_URL}/jurisdictions`);
        if (!response.ok) {
            throw new Error(`获取司法辖区列表失败: ${response.status}`);
        }
        
        const text = await response.text();
        if (!text) {
            throw new Error('服务器返回空响应');
        }
        
        jurisdictions = JSON.parse(text);
        renderJurisdictions();
    } catch (error) {
        console.error('加载司法辖区失败:', error);
        showError(`加载司法辖区列表失败: ${error.message}`);
    }
}



// 渲染司法辖区列表
function renderJurisdictions() {
    selectOptions.innerHTML = '';
    
    jurisdictions.forEach(jurisdiction => {
        const option = document.createElement('div');
        option.className = 'select-option';
        option.textContent = jurisdiction;
        option.dataset.value = jurisdiction;
        selectOptions.appendChild(option);
    });
    
    // 重置选择状态
    selectDisplay.classList.remove('selected');
    selectText.classList.add('placeholder');
}

// 渲染问题列表
function renderQuestions() {
    questionsContainer.innerHTML = '';
    
    Object.entries(questions).forEach(([id, question]) => {
        const questionItem = document.createElement('div');
        questionItem.className = 'question-item';
        questionItem.innerHTML = `
            <input type="checkbox" id="question-${id}" class="question-checkbox" value="${id}">
            <label for="question-${id}" class="question-label">${question.title}</label>
        `;
        
        questionsContainer.appendChild(questionItem);
    });
}



// DOM加载完成后初始化应用
document.addEventListener('DOMContentLoaded', initApp);

// 设置事件监听器
function setupEventListeners() {
    // 自定义下拉框事件
    selectDisplay.addEventListener('click', () => {
        const isActive = selectDisplay.classList.contains('active');
        if (isActive) {
            closeDropdown();
        } else {
            openDropdown();
        }
    });

    // 选项点击事件
    selectOptions.addEventListener('click', (e) => {
        if (e.target.classList.contains('select-option')) {
            const value = e.target.dataset.value;
            selectJurisdiction(value);
            closeDropdown();
        }
    });

    // 点击外部关闭下拉框
    document.addEventListener('click', (e) => {
        if (!customJurisdictionSelect.contains(e.target)) {
            closeDropdown();
        }
    });
    
    // 问题选择
    questionsContainer.addEventListener('change', (e) => {
        if (e.target.type === 'checkbox') {
            const questionId = e.target.value;
            const questionItem = e.target.closest('.question-item');
            
            // 添加选择动画
            questionItem.classList.add('selecting');
            setTimeout(() => {
                questionItem.classList.remove('selecting');
            }, 300);
            
            if (e.target.checked) {
                selectedQuestions.add(questionId);
                questionItem.classList.add('selected');
            } else {
                selectedQuestions.delete(questionId);
                questionItem.classList.remove('selected');
            }
            
            updateGenerateButton();
        }
    });
    
    // 问题项点击 - 优化版本
    questionsContainer.addEventListener('click', (e) => {
        const questionItem = e.target.closest('.question-item');
        if (questionItem) {
            const checkbox = questionItem.querySelector('input[type="checkbox"]');
            
            // 如果点击的不是checkbox本身，则触发checkbox
            if (e.target.type !== 'checkbox' && e.target.tagName !== 'LABEL') {
                e.preventDefault();
                checkbox.click();
            }
        }
    });
    
    // 生成报告按钮
    generateBtn.addEventListener('click', generateReport);
// 使用事件委托确保动态元素事件绑定
 document.addEventListener('click', function(event) {
   if (event.target.matches('#exportWordBtn')) {
     exportWordDocument();
   }
 });
}

// 更新生成按钮状态
function updateGenerateButton() {
    const hasJurisdiction = selectedJurisdiction !== '';
    const hasQuestions = selectedQuestions.size > 0;
    generateBtn.disabled = !(hasJurisdiction && hasQuestions);
}

// 生成报告
async function generateReport() {
    if (!selectedJurisdiction) {
        showError('请选择司法辖区');
        return;
    }
    
    // 按问题ID的数字顺序排序（1,2,3,4,5,6,7）
    const questionIds = Array.from(selectedQuestions).sort((a, b) => parseInt(a) - parseInt(b));
    
    if (questionIds.length === 0) {
        showError('请选择至少一个问题');
        return;
    }
    
    // 显示加载状态
    setLoadingState(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/research`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                jurisdiction: selectedJurisdiction,
                questions: questionIds
            })
        });
        
        if (!response.ok) {
            const text = await response.text();
            let errorMsg = '生成报告失败';
            try {
                const error = JSON.parse(text);
                errorMsg = error.error || errorMsg;
            } catch (e) {
                errorMsg = text || errorMsg;
            }
            throw new Error(errorMsg);
        }
        
        const text = await response.text();
        if (!text) {
            throw new Error('服务器返回空响应');
        }
        
        const result = JSON.parse(text);
        displayReport(result);
        
    } catch (error) {
        console.error('生成报告失败:', error);
        showError(error.message || '生成报告失败，请重试');
    } finally {
        setLoadingState(false);
    }
}

// 设置加载状态
function setLoadingState(loading) {
    const btnText = generateBtn.querySelector('.btn-text');
    
    if (loading) {
        btnText.textContent = '生成中...';
        generateBtn.disabled = true;
    } else {
        btnText.textContent = '生成报告';
        updateGenerateButton();
    }
}

// 导出Word文档
async function exportWordDocument() {
    const reportContent = document.getElementById('reportContent').innerText;
    
    if (!reportContent || !selectedJurisdiction) {
        showError('没有可导出的报告内容');
        return;
    }
    
    try {
        // 显示导出状态
        const exportBtn = document.getElementById('exportWordBtn');
        const originalText = exportBtn.textContent;
        exportBtn.textContent = '📄 导出中...';
        exportBtn.disabled = true;
        
        const response = await fetch(`${API_BASE_URL}/export-word`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                report: reportContent,
                jurisdiction: selectedJurisdiction
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || '导出失败');
        }
        
        // 获取文件名
        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = `法律检索报告_${selectedJurisdiction}_${new Date().toISOString().slice(0,10)}.docx`;
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
            if (filenameMatch) {
                filename = filenameMatch[1].replace(/['"]/g, '');
            }
        }
        
        // 下载文件
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        // 显示成功消息
        showSuccess('Word文档已成功下载！');
        
    } catch (error) {
        console.error('导出Word文档失败:', error);
        showError(error.message || '导出Word文档失败，请重试');
    } finally {
        // 恢复按钮状态
        const exportBtn = document.getElementById('exportWordBtn');
        exportBtn.textContent = '📄 导出Word文档';
        exportBtn.disabled = false;
    }
}

function displayReport(result) {
    // 显示报告标题
    document.getElementById('reportTitleContainer').innerHTML = `
        <h3>出海目标国数据隐私准入法律检索报告</h3>
        <p class="report-meta">生成时间: ${new Date().toLocaleString('zh-CN')}</p>
    `;
    
    // 直接显示格式化后的报告内容
    reportContent.innerHTML = `<div class="report-content-text">${formatReportContent(result.report)}</div>`;
const exportBtn = document.getElementById('exportWordBtn');
if (exportBtn) {
    exportBtn.classList.add('visible');
    exportBtn.style.display = 'block';
    // 强制移除可能隐藏样式
    exportBtn.classList.remove('hidden');
    exportBtn.removeAttribute('hidden');
}
    
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// 格式化报告内容
function formatReportContent(content) {
    // 将换行符转换为HTML换行标签，移除加粗和斜体样式
    return content
        .replace(/\n/g, '<br>')
        .replace(/((一) [^\n]+)/g, '<h3>$1</h3>');
}

// 显示错误信息
function showError(message) {
    alert('❌ ' + message);
}

// 显示成功信息
function showSuccess(message) {
    alert('✅ ' + message);
}

// 自定义下拉框辅助函数
function openDropdown() {
    selectDisplay.classList.add('active');
    selectOptions.classList.add('show');
}

function closeDropdown() {
    selectDisplay.classList.remove('active');
    selectOptions.classList.remove('show');
}

function selectJurisdiction(value) {
    selectedJurisdiction = value;
    selectText.textContent = value;
    selectText.classList.remove('placeholder');
    
    // 添加选中样式到显示区域
    selectDisplay.classList.add('selected');
    
    // 添加选择动画
    selectDisplay.classList.add('selecting');
    setTimeout(() => {
        selectDisplay.classList.remove('selecting');
    }, 300);
    
    // 更新选中状态
    selectOptions.querySelectorAll('.select-option').forEach(option => {
        option.classList.remove('selected');
        if (option.dataset.value === value) {
            option.classList.add('selected');
        }
    });
    
    updateGenerateButton();
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', initApp);