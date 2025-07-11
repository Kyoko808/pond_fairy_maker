document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const fairyCard = document.getElementById('fairy-card');
    const serverUrl = 'http://127.0.0.1:8000'; // Define server URL for local development

    generateBtn.addEventListener('click', async () => {
        fairyCard.classList.add('hidden');
        // Optional: Add a loading spinner here

        try {
            // Fetch fairy text from backend
            const textResponse = await fetch(`${serverUrl}/generate_fairy_text`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}),
            });
            const fairyData = await textResponse.json();

            if (fairyData.error) {
                // Provide more detailed error feedback to the user
                let userMessage = `妖精の生成中にエラーが発生しました。\n\n詳細: ${fairyData.error}`;
                if (fairyData.error.includes("GEMINI_API_KEY")) {
                    userMessage = "APIキーが設定されていないか、無効です。サーバー側の設定を確認してください。";
                }
                console.error('Error generating fairy text:', fairyData.error);
                alert(userMessage);
                return;
            }

            // Update fairy card with generated text
            document.getElementById('fairy-name').textContent = fairyData.name || '不明な妖精';
            document.getElementById('fairy-reading').textContent = fairyData.reading || '不明';
            document.getElementById('fairy-feature').textContent = fairyData.feature || '不明';
            document.getElementById('fairy-behavior').textContent = fairyData.behavior || '不明';
            document.getElementById('fairy-location').textContent = fairyData.location || '不明';
            document.getElementById('fairy-symbolism').textContent = fairyData.symbolism || '不明';

            // Generate image (using the generated fairy name for the prompt)
            const imagePrompt = `A melancholic swamp fairy named ${fairyData.name || 'Mysterious Fairy'} stands beside a misty marsh under twilight. The atmosphere is eerie and dreamy, with whimsical, surreal, gothic, and antique elements, in the style of Mark Ryden. Lighting is soft and sepia-toned, evoking a mysterious fairy tale.`;
            const imageResponse = await fetch(`${serverUrl}/generate_image`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: imagePrompt }),
            });
            const imageData = await imageResponse.json();

            const fairyImage = document.getElementById('fairy-image');
            if (imageData.image_url) {
                fairyImage.src = imageData.image_url;
                fairyImage.classList.remove('hidden');
            } else {
                console.error('Error generating image:', imageData.error);
                fairyImage.src = '';
                fairyImage.classList.add('hidden');
            }

            fairyCard.classList.remove('hidden');

        } catch (error) {
            console.error('An unexpected error occurred:', error);
            alert('サーバーへの接続に失敗しました。サーバーが起動しているか、URLが正しいか確認してください。');
        }
    });
});