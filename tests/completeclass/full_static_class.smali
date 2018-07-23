.class public final Lutil/a/z/A/b;
.super Ljava/lang/Object;


# static fields
.field private static final a:[B


# direct methods
.method static constructor <clinit>()V
    .locals 3

    const/16 v0, 0x21

    new-array v0, v0, [B

    fill-array-data v0, :array_0

    sput-object v0, Lutil/a/z/A/b;->a:[B

    return-void

    :array_0
    .array-data 1
        0x5t
        0x74t
        0x8t
        0x3ft
        -0x3t
        -0x1ft
        -0x19t
        0x54t
        -0x4et
        -0xft
        0x4et
        -0x53t
        -0xct
        0x4t
        -0x5t
        0x47t
        -0x54t
        -0x8t
        0x4dt
        -0x49t
        -0x10t
        0x5t
        -0x13t
        0x4et
        -0x53t
        -0x6t
        -0xat
        0x4ft
        -0x4at
        -0x18t
        0xat
        -0xft
        -0x6t
    .end array-data
.end method

.method private static a(III)Ljava/lang/String;
    .locals 6

    sget-object v4, Lutil/a/z/A/b;->a:[B

    const/4 v5, 0x0

    mul-int/lit8 p1, p1, 0x2

    rsub-int/lit8 p1, p1, 0x4d

    mul-int/lit8 p2, p2, 0x1b

    add-int/lit8 p2, p2, 0x2

    new-instance v0, Ljava/lang/String;

    rsub-int/lit8 p0, p0, 0x5

    new-array v1, p2, [B

    add-int/lit8 p2, p2, -0x1

    goto :goto_1

    :goto_0
    neg-int v2, v2

    add-int/lit8 p0, p0, 0x1

    add-int/2addr v2, p1

    add-int/lit8 p1, v2, -0x5

    :goto_1
    int-to-byte v2, p1

    aput-byte v2, v1, v5

    move v2, v5

    add-int/lit8 v5, v5, 0x1

    if-ne v2, p2, :cond_0

    const/4 v2, 0x0

    invoke-direct {v0, v1, v2}, Ljava/lang/String;-><init>([BI)V

    return-object v0

    :cond_0
    aget-byte v2, v4, p0

    goto :goto_0
.end method

.method public static a()Lutil/a/z/A/a;
    .locals 2

    invoke-static {}, Lutil/a/z/A/b;->c()[B

    move-result-object v0

    :try_start_0
    invoke-static {v0}, Lutil/a/z/A/a;->e([B)Lutil/a/z/A/a;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    move-result-object v1

    invoke-static {v0}, Lutil/a/z/b/d;->a([B)V

    return-object v1

    :catchall_0
    move-exception v1

    invoke-static {v0}, Lutil/a/z/b/d;->a([B)V

    throw v1
.end method

.method public static b()V
    .locals 4

    invoke-static {}, Lutil/a/z/A/a;->b()V

    invoke-static {}, Lutil/a/z/a/a;->a()Lutil/a/z/A/c;

    move-result-object v3

    invoke-interface {v3}, Lutil/a/z/A/c;->a()V

    const/4 v0, 0x1

    const/4 v1, 0x0

    const/4 v2, 0x0

    invoke-static {v0, v1, v2}, Lutil/a/z/A/b;->a(III)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/String;->intern()Ljava/lang/String;

    move-result-object v0

    invoke-interface {v3, v0}, Lutil/a/z/A/c;->d(Ljava/lang/String;)V

    return-void
.end method

.method private static c()[B
    .locals 5

    invoke-static {}, Lutil/a/z/a/a;->a()Lutil/a/z/A/c;

    move-result-object v4

    :try_start_0
    invoke-interface {v4}, Lutil/a/z/A/c;->a()V

    const/4 v0, 0x1

    const/4 v1, 0x0

    const/4 v2, 0x0

    invoke-static {v0, v1, v2}, Lutil/a/z/A/b;->a(III)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/String;->intern()Ljava/lang/String;

    move-result-object v0

    invoke-interface {v4, v0}, Lutil/a/z/A/c;->a(Ljava/lang/String;)Z

    move-result v0

    if-nez v0, :cond_0

    const/4 v0, 0x1

    const/4 v1, 0x0

    const/4 v2, 0x0

    invoke-static {v0, v1, v2}, Lutil/a/z/A/b;->a(III)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/String;->intern()Ljava/lang/String;

    move-result-object v0

    invoke-interface {v4, v0}, Lutil/a/z/A/c;->c(Ljava/lang/String;)V

    :cond_0
    const/4 v0, 0x1

    const/4 v1, 0x0

    const/4 v2, 0x0

    invoke-static {v0, v1, v2}, Lutil/a/z/A/b;->a(III)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/String;->intern()Ljava/lang/String;

    move-result-object v0

    invoke-interface {v4, v0}, Lutil/a/z/A/c;->b(Ljava/lang/String;)[B
    :try_end_0
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_0

    move-result-object v4

    goto :goto_0

    :catch_0
    const/4 v0, 0x0

    return-object v0

    :goto_0
    if-nez v4, :cond_1

    new-instance v0, Lutil/a/z/A/d;

    const/4 v1, 0x0

    const/4 v2, 0x1

    const/4 v3, 0x1

    invoke-static {v1, v2, v3}, Lutil/a/z/A/b;->a(III)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/String;->intern()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v0, v1}, Lutil/a/z/A/d;-><init>(Ljava/lang/String;)V

    throw v0

    :cond_1
    return-object v4
.end method

