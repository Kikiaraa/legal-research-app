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
const jurisdictionSelect = document.getElementById('jurisdictionSelect');
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
        if (!response.ok) throw new Error('获取问题列表失败');
        
        questions = await response.json();
        renderQuestions();
    } catch (error) {
        console.error('加载问题失败:', error);
        showError('加载问题列表失败');
    }
}

// 加载司法辖区列表
async function loadJurisdictions() {
    try {
        const response = await fetch(`${API_BASE_URL}/jurisdictions`);
        if (!response.ok) throw new Error('获取司法辖区列表失败');
        
        jurisdictions = await response.json();
        renderJurisdictions();
    } catch (error) {
        console.error('加载司法辖区失败:', error);
        showError('加载司法辖区列表失败');
    }
}



// 渲染司法辖区列表
function renderJurisdictions() {
    jurisdictionSelect.innerHTML = '<option value="">请选择司法辖区</option>';
    
    jurisdictions.forEach(jurisdiction => {
        const option = document.createElement('option');
        option.value = jurisdiction;
        option.textContent = jurisdiction;
        jurisdictionSelect.appendChild(option);
    });
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
    // 司法辖区选择
    jurisdictionSelect.addEventListener('change', (e) => {
        selectedJurisdiction = e.target.value;
        
        // 添加选择动画
        e.target.classList.add('selecting');
        setTimeout(() => {
            e.target.classList.remove('selecting');
        }, 400);
        
        updateGenerateButton();
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
    
    // 问题项点击
    questionsContainer.addEventListener('click', (e) => {
        const questionItem = e.target.closest('.question-item');
        if (questionItem && e.target.type !== 'checkbox') {
            const checkbox = questionItem.querySelector('input[type="checkbox"]');
            checkbox.click();
        }
    });
    
    // 生成报告按钮
    generateBtn.addEventListener('click', generateReport);
// 使用事件委托确保动态元素事件绑定
 document.addEventListener('click', function(event) {
   if (event.target.matches('#copyReportBtn')) {
     copyReport();
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
    
    const questionIds = Array.from(selectedQuestions);
    
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
            const error = await response.json();
            throw new Error(error.error || '生成报告失败');
        }
        
        const result = await response.json();
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

// 显示报告
async function copyReport() {
  const reportContent = document.getElementById('reportContent').innerText;
  try {
    await navigator.clipboard.writeText(reportContent);
    alert('报告已成功复制到剪贴板！');
  } catch (err) {
    alert('复制失败: ' + err.message);
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
const copyBtn = document.getElementById('copyReportBtn');
if (copyBtn) {
    copyBtn.classList.add('visible');
copyBtn.style.display = 'block';
    // 强制移除可能隐藏样式
    copyBtn.classList.remove('hidden');
    copyBtn.removeAttribute('hidden');
    // 确保点击事件绑定

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
    alert(message); // 简单的错误提示，可以后续改进为更好的UI
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', initApp);