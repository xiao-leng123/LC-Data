document.addEventListener("DOMContentLoaded", function() {
    // 初始化显示主页内容
    showOnly('home');

    // 设置菜单项的点击事件
    document.getElementById("link-home").addEventListener("click", function() {
        showOnly('home');
    });

    document.getElementById("link-temperature-analysis").addEventListener("click", function() {
        showOnly('temperature-analysis');
    });

    document.getElementById("link-air-quality-analysis").addEventListener("click", function() {
        showOnly('air-quality-analysis');
    });

    document.getElementById("link-wind-analysis").addEventListener("click", function() {
        showOnly('wind-analysis');
    });

    document.getElementById("link-correlation-analysis").addEventListener("click", function() {
        showOnly('correlation-analysis');
    });

    function showOnly(analysisId) {
        window.scrollTo(0, 0);

        // 隐藏所有内容
        document.querySelectorAll('.content > div').forEach(div => {
            div.style.display = 'none';
        });

        // 显示选中的内容
        const selectedAnalysis = document.getElementById(analysisId);
        selectedAnalysis.style.display = 'block';

        // 为选中的分析容器中的每个图表添加动画
        const charts = selectedAnalysis.querySelectorAll('.chart');
        charts.forEach((chart, index) => {
            anime({
                targets: chart,
                opacity: [0, 1], // 透明度从0变化到1
                translateY: [20, 0], // 从下方20px处移动到其正常位置
                delay: anime.stagger(200, {start: 300}), // 每个图表动画之间的延迟时间
                duration: 1500, // 动画持续时间
                easing: 'easeOutExpo' // 缓动函数
            });
        });
    }
});