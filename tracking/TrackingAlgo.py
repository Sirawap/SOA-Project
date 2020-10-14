def calculateDistance(distance, senderRoom, receiverRoom):
  covidDistance = 5
  if senderRoom is not receiverRoom:
    return False
  if distance <= covidDistance:
    return True
  return False
