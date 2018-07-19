# {"p0": 1, "p1": 1, "p2": -1, "ret": "value cannot be null"}

.method private static a(III)Ljava/lang/String;

    .locals 6

    const/16 v4, 0x2c

    new-array v4, v4, [B

    fill-array-data v4, :array_0

    add-int/lit8 p2, p2, 0x4

    mul-int/lit8 p1, p1, 0x2b

    add-int/lit8 p1, p1, 0x4b

    mul-int/lit8 p0, p0, 0x2

    rsub-int/lit8 p0, p0, 0x16

    new-instance v0, Ljava/lang/String;

    const/4 v5, 0x0

    new-array v1, p0, [B

    goto :goto_1

    :goto_0
    sub-int/2addr p1, v2

    :goto_1
    move v2, v5

    add-int/lit8 p2, p2, 0x1

    add-int/lit8 v5, v5, 0x1

    int-to-byte v3, p1

    aput-byte v3, v1, v2

    if-ne v5, p0, :cond_0

    const/4 v2, 0x0

    invoke-direct {v0, v1, v2}, Ljava/lang/String;-><init>([BI)V

    return-object v0

    :cond_0
    aget-byte v2, v4, p2

    goto :goto_0


    :array_0
    .array-data 1
        0x21t
        0x36t
        0x3bt
        -0x1ft
        0x15t
        -0xbt
        -0x9t
        0x10t
        0x45t
        -0x43t
        0x2t
        -0xdt
        0x0t
        -0x1t
        -0x5t
        0x54t
        -0x42t
        -0x3t
        0x45t
        -0x4et
        -0x7t
        0x9t
        0x0t
        -0x1at
        -0x14t
        0x59t
        -0x49t
        -0xat
        0x53t
        -0x4et
        -0x1t
        -0x5t
        0x54t
        -0x57t
        0x5t
        0x9t
        -0xbt
        0x0t
        0xft
        -0x9t
        0x4et
        -0x59t
        0x14t
        -0xft
    .end array-data
.end method

