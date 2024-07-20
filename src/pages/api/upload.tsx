// pages/api/upload.ts
import { NextApiRequest, NextApiResponse } from "next";

import multer from "multer";
import { Request as ExpressRequest } from "express";

// Set up multer for file storage
const upload = multer({
  storage: multer.diskStorage({
    destination: "./public/uploads", 
    filename: (req, file, cb) => cb(null, file.originalname),
  }),
});

// // Create an API route using nextConnect
// const apiRoute = nextConnect<NextApiRequest, NextApiResponse>({
//   onError(error:Error, req:NextApiRequest, res:NextApiResponse) {
//     res.status(501).json({ error: `Sorry something happened! ${error.message}` });
//   },
//   onNoMatch(req:NextApiRequest, res:NextApiResponse) {
//     res.status(405).json({ error: `Method '${req.method}' Not Allowed` });
//   },
// });
// // Configure the route to handle file uploads
// apiRoute.use(upload.single("file"));

// apiRoute.post((req:ExpressRequest, res:NextApiResponse) => {
//   res.status(200).json({ data: "File uploaded successfully" });
// });

// export default apiRoute;

export const config = {
  api: {
    bodyParser: false, // Disable body parsing, as multer will handle it
  },
};
