const fs = require('fs');
const path = require('path');

// Define the path to your HTML file
const htmlFilePath = path.join(__dirname, '..', '..', '..', 'templates', 'order.html');

// Get the filenames in the build/static/js and build/static/css directories
const jsFilename = fs.readdirSync(path.join(__dirname, 'build', 'static', 'js')).find(file => file.startsWith('main.'));
const cssFilename = fs.readdirSync(path.join(__dirname, 'build', 'static', 'css')).find(file => file.startsWith('main.'));


// Read the HTML file
fs.readFile(htmlFilePath, 'utf8', (err, data) => {
    if (err) {
        console.error(err);
        return;
    }

    // Replace the old file paths with the new ones
    let updatedData = data.replace(/main\.[a-z0-9]+\.js/g, jsFilename);
    updatedData = updatedData.replace(/main\.[a-z0-9]+\.css/g, cssFilename);

    // Write the updated content back to the HTML file
    fs.writeFile(htmlFilePath, updatedData, 'utf8', (err) => {
        if (err) {
            console.error(err);
            return;
        }

        console.log('File paths updated successfully!');
    });
});