echo OFF

call ./build.bat
cd ..

echo Starting server
cd server
npm start