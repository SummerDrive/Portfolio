import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";

const s3 = new S3Client({ region: "ap-northeast-1" });

export const handler = async () => {
  const command = new GetObjectCommand({
    Bucket: "summerdrivewebmaptest",
    Key: "RaceID.csv"
  });

  const response = await s3.send(command);
  const body = await response.Body.transformToString();

  return {
    statusCode: 200,
    headers: {
      "Content-Type": "text/plain"
    },
    body: body
  };
};