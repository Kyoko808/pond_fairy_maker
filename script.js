document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const fairyCard = document.getElementById('fairy-card');

    generateBtn.addEventListener('click', async () => {
        // Hide card and show loading indicator (optional)
        fairyCard.classList.add('hidden');
        // You might want to add a loading spinner here

        try {
            // Fetch fairy text from backend
            const textResponse = await fetch('/generate_fairy_text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}), // No specific input needed for text generation
            });
            const fairyData = await textResponse.json();

            if (fairyData.error) {
                console.error('Error generating fairy text:', fairyData.error);
                alert('妖精のテキスト生成中にエラーが発生しました: ' + fairyData.error);
                return;
            }

            // Update fairy card with generated text
            document.getElementById('fairy-name').textContent = fairyData.name || '不明な妖精';
            document.getElementById('fairy-alias').textContent = fairyData.alias || '不明';
            document.getElementById('fairy-feature').textContent = fairyData.feature || '不明';
            document.getElementById('fairy-behavior').textContent = fairyData.behavior || '不明';
            document.getElementById('fairy-location').textContent = fairyData.location || '不明';
            document.getElementById('fairy-symbolism').textContent = fairyData.symbolism || '不明';

            // Generate image (using the generated fairy name for the prompt)
            const imagePrompt = `A melancholic swamp fairy named ${fairyData.name || 'Mysterious Fairy'} stands beside a misty marsh under twilight. The atmosphere is eerie and dreamy, with whimsical, surreal, gothic, and antique elements, in the style of Mark Ryden. Lighting is soft and sepia-toned, evoking a mysterious fairy tale.`;
            const imageResponse = await fetch('/generate_image', {
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
            alert('予期せぬエラーが発生しました。コンソールを確認してください。');
        }
    });
});